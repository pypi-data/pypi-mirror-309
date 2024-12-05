use arrow_array::builder::make_view;
use arrow_buffer::{BooleanBuffer, BufferBuilder};
use vortex_buffer::Buffer;
use vortex_dtype::{match_each_native_ptype, DType, Nullability, PType};
use vortex_error::{vortex_bail, vortex_panic, VortexResult};
use vortex_scalar::{BinaryScalar, BoolScalar, ExtScalar, Scalar, Utf8Scalar};

use crate::array::constant::ConstantArray;
use crate::array::primitive::PrimitiveArray;
use crate::array::{
    BinaryView, BoolArray, ExtensionArray, NullArray, VarBinViewArray, VIEW_SIZE_BYTES,
};
use crate::validity::Validity;
use crate::{ArrayDType, Canonical, IntoArrayData, IntoCanonical};

impl IntoCanonical for ConstantArray {
    fn into_canonical(self) -> VortexResult<Canonical> {
        let scalar = &self.owned_scalar();

        let validity = match self.dtype().nullability() {
            Nullability::NonNullable => Validity::NonNullable,
            Nullability::Nullable => match scalar.is_null() {
                true => Validity::AllInvalid,
                false => Validity::AllValid,
            },
        };

        if let Ok(b) = BoolScalar::try_from(scalar) {
            return Ok(Canonical::Bool(BoolArray::try_new(
                if b.value().unwrap_or_default() {
                    BooleanBuffer::new_set(self.len())
                } else {
                    BooleanBuffer::new_unset(self.len())
                },
                validity,
            )?));
        }

        if let Ok(s) = Utf8Scalar::try_from(scalar) {
            let value = s.value();
            let const_value = value.as_ref().map(|v| v.as_bytes());

            return canonical_byte_view(const_value, self.dtype(), self.len())
                .map(Canonical::VarBinView);
        }

        if let Ok(b) = BinaryScalar::try_from(scalar) {
            let value = b.value();
            let const_value = value.as_ref().map(|v| v.as_slice());

            return canonical_byte_view(const_value, self.dtype(), self.len())
                .map(Canonical::VarBinView);
        }

        if let Ok(ptype) = PType::try_from(scalar.dtype()) {
            return match_each_native_ptype!(ptype, |$P| {
                Ok(Canonical::Primitive(PrimitiveArray::from_vec::<$P>(
                    vec![$P::try_from(scalar).unwrap_or_else(|_| $P::default()); self.len()],
                    validity,
                )))
            });
        }

        if matches!(self.dtype(), DType::Null) {
            return Ok(Canonical::Null(NullArray::new(self.len())));
        }

        if let Ok(s) = ExtScalar::try_from(scalar) {
            let DType::Extension(ext_dtype) = s.dtype() else {
                vortex_panic!("ExtScalar has a non-ext dtype {}", s.dtype());
            };

            let storage_dtype = ext_dtype.storage_dtype();
            let storage_scalar = Scalar::new(storage_dtype.clone(), s.value().clone());
            let storage_array = ConstantArray::new(storage_scalar, self.len()).into_array();
            return ExtensionArray::new(ext_dtype.clone(), storage_array).into_canonical();
        }

        vortex_bail!("Unsupported scalar type {}", self.dtype())
    }
}

fn canonical_byte_view(
    scalar_bytes: Option<&[u8]>,
    dtype: &DType,
    len: usize,
) -> VortexResult<VarBinViewArray> {
    match scalar_bytes {
        None => {
            let views = ConstantArray::new(0u8, len * VIEW_SIZE_BYTES);

            VarBinViewArray::try_new(
                views.into_array(),
                Vec::new(),
                dtype.clone(),
                Validity::AllInvalid,
            )
        }
        Some(scalar_bytes) => {
            // Create a view to hold the scalar bytes.
            // If the scalar cannot be inlined, allocate a single buffer large enough to hold it.
            let view: u128 = make_view(scalar_bytes, 0, 0);
            let mut buffers = Vec::new();
            if scalar_bytes.len() >= BinaryView::MAX_INLINED_SIZE {
                buffers.push(
                    PrimitiveArray::new(
                        Buffer::from(scalar_bytes),
                        PType::U8,
                        Validity::NonNullable,
                    )
                    .into_array(),
                );
            }

            // Clone our constant view `len` times.
            // TODO(aduffy): switch this out for a ConstantArray once we
            //   add u128 PType, see https://github.com/spiraldb/vortex/issues/1110
            let mut views = BufferBuilder::<u128>::new(len);
            views.append_n(len, view);
            let views =
                PrimitiveArray::new(views.finish().into(), PType::U8, Validity::NonNullable)
                    .into_array();

            let validity = if dtype.nullability() == Nullability::NonNullable {
                Validity::NonNullable
            } else {
                Validity::AllValid
            };

            VarBinViewArray::try_new(views, buffers, dtype.clone(), validity)
        }
    }
}

#[cfg(test)]
mod tests {
    use vortex_dtype::{DType, Nullability};
    use vortex_scalar::Scalar;

    use crate::array::ConstantArray;
    use crate::compute::unary::scalar_at;
    use crate::stats::{ArrayStatistics as _, StatsSet};
    use crate::{IntoArrayData as _, IntoCanonical};

    #[test]
    fn test_canonicalize_null() {
        let const_null = ConstantArray::new(Scalar::null(DType::Null), 42);
        let actual = const_null.into_canonical().unwrap().into_null().unwrap();
        assert_eq!(actual.len(), 42);
        assert_eq!(scalar_at(actual, 33).unwrap(), Scalar::null(DType::Null));
    }

    #[test]
    fn test_canonicalize_const_str() {
        let const_array = ConstantArray::new("four".to_string(), 4);

        // Check all values correct.
        let canonical = const_array
            .into_canonical()
            .unwrap()
            .into_varbinview()
            .unwrap();

        assert_eq!(canonical.len(), 4);

        for i in 0..=3 {
            assert_eq!(scalar_at(&canonical, i).unwrap(), "four".into(),);
        }
    }

    #[test]
    fn test_canonicalize_propagates_stats() {
        let scalar = Scalar::bool(true, Nullability::NonNullable);
        let const_array = ConstantArray::new(scalar.clone(), 4).into_array();
        let stats = const_array.statistics().to_set();

        let canonical = const_array.into_canonical().unwrap();
        let canonical_stats = canonical.statistics().to_set();

        assert_eq!(canonical_stats, StatsSet::constant(scalar, 4));
        assert_eq!(canonical_stats, stats);
    }
}
