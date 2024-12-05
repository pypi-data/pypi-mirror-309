use std::fmt::{Debug, Display};

use serde::{Deserialize, Serialize};
use vortex_array::aliases::hash_map::HashMap;
use vortex_array::array::visitor::{AcceptArrayVisitor, ArrayVisitor};
use vortex_array::array::PrimitiveArray;
use vortex_array::compute::unary::scalar_at;
use vortex_array::compute::{search_sorted, search_sorted_u64_many, SearchSortedSide};
use vortex_array::encoding::ids;
use vortex_array::stats::{ArrayStatistics, ArrayStatisticsCompute, Stat, StatsSet};
use vortex_array::validity::{ArrayValidity, LogicalValidity, Validity, ValidityMetadata};
use vortex_array::variants::{ArrayVariants, PrimitiveArrayTrait};
use vortex_array::{
    impl_encoding, ArrayDType, ArrayData, ArrayTrait, Canonical, IntoArrayData, IntoArrayVariant,
    IntoCanonical,
};
use vortex_dtype::{DType, PType};
use vortex_error::{vortex_bail, VortexExpect as _, VortexResult};
use vortex_scalar::Scalar;

use crate::compress::{runend_decode, runend_encode};

impl_encoding!("vortex.runend", ids::RUN_END, RunEnd);

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RunEndMetadata {
    validity: ValidityMetadata,
    ends_ptype: PType,
    num_runs: usize,
    offset: usize,
}

impl Display for RunEndMetadata {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        Debug::fmt(self, f)
    }
}

impl RunEndArray {
    pub fn try_new(ends: ArrayData, values: ArrayData, validity: Validity) -> VortexResult<Self> {
        let length = if ends.is_empty() {
            0
        } else {
            scalar_at(&ends, ends.len() - 1)?.as_ref().try_into()?
        };
        Self::with_offset_and_length(ends, values, validity, 0, length)
    }

    pub(crate) fn with_offset_and_length(
        ends: ArrayData,
        values: ArrayData,
        validity: Validity,
        offset: usize,
        length: usize,
    ) -> VortexResult<Self> {
        if values.dtype().nullability() != validity.nullability() {
            vortex_bail!(
                "invalid validity {:?} for dtype {}",
                validity,
                values.dtype()
            );
        }

        if offset != 0 && !ends.is_empty() {
            let first_run_end: usize = scalar_at(&ends, 0)?.as_ref().try_into()?;
            if first_run_end <= offset {
                vortex_bail!("First run end {first_run_end} must be bigger than offset {offset}");
            }
        }

        if !ends.dtype().is_unsigned_int() || ends.dtype().is_nullable() {
            vortex_bail!(MismatchedTypes: "non-nullable unsigned int", ends.dtype());
        }
        if !ends.statistics().compute_is_strict_sorted().unwrap_or(true) {
            vortex_bail!("Ends array must be strictly sorted");
        }

        let dtype = values.dtype().clone();
        let metadata = RunEndMetadata {
            validity: validity.to_metadata(length)?,
            ends_ptype: PType::try_from(ends.dtype())?,
            num_runs: ends.len(),
            offset,
        };

        let stats = if matches!(validity, Validity::AllValid | Validity::NonNullable) {
            let ends_len = ends.len();
            let is_constant = ends_len <= 1;
            StatsSet::from(HashMap::from([
                (Stat::IsConstant, is_constant.into()),
                (Stat::RunCount, (ends_len as u64).into()),
            ]))
        } else if matches!(validity, Validity::AllInvalid) {
            StatsSet::nulls(length, &dtype)
        } else {
            StatsSet::new()
        };

        let mut children = Vec::with_capacity(3);
        children.push(ends);
        children.push(values);
        if let Some(a) = validity.into_array() {
            children.push(a)
        }

        Self::try_from_parts(dtype, length, metadata, children.into(), stats)
    }

    /// Convert the given logical index to an index into the `values` array
    pub fn find_physical_index(&self, index: usize) -> VortexResult<usize> {
        search_sorted(&self.ends(), index + self.offset(), SearchSortedSide::Right)
            .map(|s| s.to_ends_index(self.ends().len()))
    }

    /// Convert a batch of logical indices into an index for the values. Expects indices to be adjusted by offset unlike
    /// [Self::find_physical_index]
    ///
    /// See: [find_physical_index][Self::find_physical_index].
    pub fn find_physical_indices(&self, indices: &[u64]) -> VortexResult<Vec<usize>> {
        search_sorted_u64_many(
            &self.ends(),
            indices,
            &vec![SearchSortedSide::Right; indices.len()],
        )
        .map(|results| {
            results
                .iter()
                .map(|result| result.to_ends_index(self.ends().len()))
                .collect()
        })
    }

    /// Run the array through run-end encoding.
    pub fn encode(array: ArrayData) -> VortexResult<Self> {
        if let Ok(parray) = PrimitiveArray::try_from(array) {
            let (ends, values) = runend_encode(&parray);
            Self::try_new(ends.into_array(), values.into_array(), parray.validity())
        } else {
            vortex_bail!("REE can only encode primitive arrays")
        }
    }

    pub fn validity(&self) -> Validity {
        self.metadata().validity.to_validity(|| {
            self.as_ref()
                .child(2, &Validity::DTYPE, self.len())
                .vortex_expect("RunEndArray: validity child")
        })
    }

    /// The offset that the `ends` is relative to.
    ///
    /// This is generally zero for a "new" array, and non-zero after a slicing operation.
    #[inline]
    pub fn offset(&self) -> usize {
        self.metadata().offset
    }

    /// The encoded "ends" of value runs.
    ///
    /// The `i`-th element indicates that there is a run of the same value, beginning
    /// at `ends[i]` (inclusive) and terminating at `ends[i+1]` (exclusive).
    #[inline]
    pub fn ends(&self) -> ArrayData {
        self.as_ref()
            .child(
                0,
                &DType::from(self.metadata().ends_ptype),
                self.metadata().num_runs,
            )
            .vortex_expect("RunEndArray is missing its run ends")
    }

    /// The scalar values.
    ///
    /// The `i`-th element is the scalar value for the `i`-th repeated run. The run begins
    /// at `ends[i]` (inclusive) and terminates at `ends[i+1]` (exclusive).
    #[inline]
    pub fn values(&self) -> ArrayData {
        self.as_ref()
            .child(1, self.dtype(), self.metadata().num_runs)
            .vortex_expect("RunEndArray is missing its values")
    }
}

impl ArrayTrait for RunEndArray {}

impl ArrayVariants for RunEndArray {
    fn as_primitive_array(&self) -> Option<&dyn PrimitiveArrayTrait> {
        Some(self)
    }
}

impl PrimitiveArrayTrait for RunEndArray {}

impl ArrayValidity for RunEndArray {
    fn is_valid(&self, index: usize) -> bool {
        self.validity().is_valid(index)
    }

    fn logical_validity(&self) -> LogicalValidity {
        self.validity().to_logical(self.len())
    }
}

impl IntoCanonical for RunEndArray {
    fn into_canonical(self) -> VortexResult<Canonical> {
        let pends = self.ends().into_primitive()?;
        let pvalues = self.values().into_primitive()?;
        runend_decode(&pends, &pvalues, self.validity(), self.offset(), self.len())
            .map(Canonical::Primitive)
    }
}

impl AcceptArrayVisitor for RunEndArray {
    fn accept(&self, visitor: &mut dyn ArrayVisitor) -> VortexResult<()> {
        visitor.visit_child("ends", &self.ends())?;
        visitor.visit_child("values", &self.values())?;
        visitor.visit_validity(&self.validity())
    }
}

impl ArrayStatisticsCompute for RunEndArray {
    fn compute_statistics(&self, stat: Stat) -> VortexResult<StatsSet> {
        let maybe_stat = match stat {
            Stat::Min | Stat::Max => self.values().statistics().compute(stat),
            Stat::NullCount => Some(Scalar::from(self.validity().null_count(self.len())?)),
            Stat::IsSorted => Some(Scalar::from(
                self.values()
                    .statistics()
                    .compute_is_sorted()
                    .unwrap_or(false)
                    && self.logical_validity().all_valid(),
            )),
            _ => None,
        };

        let mut stats = StatsSet::new();
        if let Some(stat_value) = maybe_stat {
            stats.set(stat, stat_value);
        }
        Ok(stats)
    }
}

#[cfg(test)]
mod tests {
    use vortex_array::compute::unary::scalar_at;
    use vortex_array::validity::Validity;
    use vortex_array::{ArrayDType, IntoArrayData};
    use vortex_dtype::{DType, Nullability, PType};

    use crate::RunEndArray;

    #[test]
    fn new() {
        let arr = RunEndArray::try_new(
            vec![2u32, 5, 10].into_array(),
            vec![1i32, 2, 3].into_array(),
            Validity::NonNullable,
        )
        .unwrap();
        assert_eq!(arr.len(), 10);
        assert_eq!(
            arr.dtype(),
            &DType::Primitive(PType::I32, Nullability::NonNullable)
        );

        // 0, 1 => 1
        // 2, 3, 4 => 2
        // 5, 6, 7, 8, 9 => 3
        assert_eq!(scalar_at(arr.as_ref(), 0).unwrap(), 1.into());
        assert_eq!(scalar_at(arr.as_ref(), 2).unwrap(), 2.into());
        assert_eq!(scalar_at(arr.as_ref(), 5).unwrap(), 3.into());
        assert_eq!(scalar_at(arr.as_ref(), 9).unwrap(), 3.into());
    }
}
