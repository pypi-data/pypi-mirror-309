use itertools::Itertools;
use vortex_array::aliases::hash_set::HashSet;
use vortex_array::array::{Struct, StructArray};
use vortex_array::compress::compute_pruning_stats;
use vortex_array::encoding::EncodingRef;
use vortex_array::stats::ArrayStatistics as _;
use vortex_array::variants::StructArrayTrait;
use vortex_array::{ArrayData, ArrayDef, IntoArrayData};
use vortex_error::VortexResult;

use crate::compressors::{CompressedArray, CompressionTree, EncodingCompressor};
use crate::SamplingCompressor;

#[derive(Debug)]
pub struct StructCompressor;

impl EncodingCompressor for StructCompressor {
    fn id(&self) -> &str {
        Struct::ID.as_ref()
    }

    fn cost(&self) -> u8 {
        0
    }

    fn can_compress(&self, array: &ArrayData) -> Option<&dyn EncodingCompressor> {
        StructArray::try_from(array)
            .ok()
            .map(|_| self as &dyn EncodingCompressor)
    }

    fn compress<'a>(
        &'a self,
        array: &ArrayData,
        like: Option<CompressionTree<'a>>,
        ctx: SamplingCompressor<'a>,
    ) -> VortexResult<CompressedArray<'a>> {
        let array = StructArray::try_from(array)?;
        let compressed_validity = ctx.compress_validity(array.validity())?;

        let children_trees = match like {
            Some(tree) => tree.children,
            None => vec![None; array.nfields()],
        };

        let (arrays, trees) = array
            .children()
            .zip_eq(children_trees)
            .map(|(array, like)| {
                // these are extremely valuable when reading/writing, but are potentially much more expensive
                // to compute post-compression. That's because not all encodings implement stats, so we would
                // potentially have to canonicalize during writes just to get stats, which would be silly.
                // Also, we only really require them for column chunks, not for every array.
                compute_pruning_stats(&array)?;
                ctx.compress(&array, like.as_ref())
            })
            .process_results(|iter| iter.map(|x| (x.array, x.path)).unzip())?;

        Ok(CompressedArray::compressed(
            StructArray::try_new(
                array.names().clone(),
                arrays,
                array.len(),
                compressed_validity,
            )?
            .into_array(),
            Some(CompressionTree::new(self, trees)),
            Some(array.statistics()),
        ))
    }

    fn used_encodings(&self) -> HashSet<EncodingRef> {
        HashSet::from([])
    }
}
