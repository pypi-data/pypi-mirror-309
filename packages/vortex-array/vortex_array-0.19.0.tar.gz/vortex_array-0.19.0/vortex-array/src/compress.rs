use vortex_error::VortexResult;

use crate::aliases::hash_set::HashSet;
use crate::encoding::EncodingRef;
use crate::stats::{ArrayStatistics as _, PRUNING_STATS};
use crate::ArrayData;

pub trait CompressionStrategy {
    fn compress(&self, array: &ArrayData) -> VortexResult<ArrayData>;

    fn used_encodings(&self) -> HashSet<EncodingRef>;
}

/// Check that compression did not alter the length of the validity array.
pub fn check_validity_unchanged(arr: &ArrayData, compressed: &ArrayData) {
    let _ = arr;
    let _ = compressed;
    #[cfg(debug_assertions)]
    {
        let old_validity = arr.with_dyn(|a| a.logical_validity().len());
        let new_validity = compressed.with_dyn(|a| a.logical_validity().len());

        debug_assert!(
            old_validity == new_validity,
            "validity length changed after compression: {old_validity} -> {new_validity}\n From tree {} To tree {}\n",
            arr.tree_display(),
            compressed.tree_display()
        );
    }
}

/// Check that compression did not alter the dtype
pub fn check_dtype_unchanged(arr: &ArrayData, compressed: &ArrayData) {
    let _ = arr;
    let _ = compressed;
    #[cfg(debug_assertions)]
    {
        use crate::ArrayDType;
        debug_assert!(
            arr.dtype() == compressed.dtype(),
            "Compression changed dtype: {} -> {}\nFrom array: {}Into array {}",
            arr.dtype(),
            compressed.dtype(),
            arr.tree_display(),
            compressed.tree_display(),
        );
    }
}

// Check that compression preserved the statistics.
pub fn check_statistics_unchanged(arr: &ArrayData, compressed: &ArrayData) {
    let _ = arr;
    let _ = compressed;
    #[cfg(debug_assertions)]
    {
        for (stat, value) in arr.statistics().to_set().into_iter() {
            debug_assert_eq!(
                compressed.statistics().get(stat),
                Some(value.clone()),
                "Compression changed {stat} from {value} to {}",
                compressed
                    .statistics()
                    .get(stat)
                    .map(|s| s.to_string())
                    .unwrap_or_else(|| "null".to_string())
            );
        }
    }
}

/// Compute pruning stats for an array.
pub fn compute_pruning_stats(arr: &ArrayData) -> VortexResult<()> {
    arr.statistics().compute_all(PRUNING_STATS).map(|_| ())
}
