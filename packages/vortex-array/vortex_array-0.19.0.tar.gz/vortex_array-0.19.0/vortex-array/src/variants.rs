//! This module defines array traits for each Vortex DType.
//!
//! When callers only want to make assumptions about the DType, and not about any specific
//! encoding, they can use these traits to write encoding-agnostic code.

use std::sync::Arc;

use vortex_dtype::field::Field;
use vortex_dtype::{DType, ExtDType, FieldNames, PType};
use vortex_error::{vortex_panic, VortexExpect as _, VortexResult};

use crate::iter::{AccessorRef, VectorizedArrayIter};
use crate::{ArrayData, ArrayTrait};

pub trait ArrayVariants {
    fn as_null_array(&self) -> Option<&dyn NullArrayTrait> {
        None
    }

    fn as_null_array_unchecked(&self) -> &dyn NullArrayTrait {
        self.as_null_array().vortex_expect("Expected NullArray")
    }

    fn as_bool_array(&self) -> Option<&dyn BoolArrayTrait> {
        None
    }

    fn as_bool_array_unchecked(&self) -> &dyn BoolArrayTrait {
        self.as_bool_array().vortex_expect("Expected BoolArray")
    }

    fn as_primitive_array(&self) -> Option<&dyn PrimitiveArrayTrait> {
        None
    }

    fn as_primitive_array_unchecked(&self) -> &dyn PrimitiveArrayTrait {
        self.as_primitive_array()
            .vortex_expect("Expected PrimitiveArray")
    }

    fn as_utf8_array(&self) -> Option<&dyn Utf8ArrayTrait> {
        None
    }

    fn as_utf8_array_unchecked(&self) -> &dyn Utf8ArrayTrait {
        self.as_utf8_array().vortex_expect("Expected Utf8Array")
    }

    fn as_binary_array(&self) -> Option<&dyn BinaryArrayTrait> {
        None
    }

    fn as_binary_array_unchecked(&self) -> &dyn BinaryArrayTrait {
        self.as_binary_array().vortex_expect("Expected BinaryArray")
    }

    fn as_struct_array(&self) -> Option<&dyn StructArrayTrait> {
        None
    }

    fn as_struct_array_unchecked(&self) -> &dyn StructArrayTrait {
        self.as_struct_array().vortex_expect("Expected StructArray")
    }

    fn as_list_array(&self) -> Option<&dyn ListArrayTrait> {
        None
    }

    fn as_list_array_unchecked(&self) -> &dyn ListArrayTrait {
        self.as_list_array().vortex_expect("Expected ListArray")
    }

    fn as_extension_array(&self) -> Option<&dyn ExtensionArrayTrait> {
        None
    }

    fn as_extension_array_unchecked(&self) -> &dyn ExtensionArrayTrait {
        self.as_extension_array()
            .vortex_expect("Expected ExtensionArray")
    }
}

pub trait NullArrayTrait: ArrayTrait {}

pub trait BoolArrayTrait: ArrayTrait {
    /// Return a new inverted version of this array.
    ///
    /// True -> False
    /// False -> True
    /// Null -> Null
    fn invert(&self) -> VortexResult<ArrayData>;

    fn true_count(&self) -> usize {
        self.statistics()
            .compute_true_count()
            .unwrap_or_else(|| self.maybe_null_indices_iter().count())
    }

    /// An iterator over the sorted indices of set values in the underlying boolean array
    /// good to array with low number of set values.
    ///
    /// # Warning
    ///
    /// The set-ness of invalid positions is undefined and not necessarily consistent within a given
    /// iterator.
    fn maybe_null_indices_iter<'a>(&'a self) -> Box<dyn Iterator<Item = usize> + 'a>;

    /// An iterator over the sorted disjoint contiguous range of set values in the underlying boolean
    /// array good for arrays with only long runs of set values.
    ///
    /// # Warning
    ///
    /// The set-ness of invalid positions is undefined and not necessarily consistent within a given
    /// iterator.
    fn maybe_null_slices_iter<'a>(&'a self) -> Box<dyn Iterator<Item = (usize, usize)> + 'a>;

    // Other possible iterators include:
    //  - True(usize) | False(usize) | Mixed(BooleanBuffer) where True/False are long runs of either
    //                                                            true or false values and mixed
    //                                                            is everything else
    //  - T|F + [(usize, BooleanBuffer)] where usize represents an offset into the original array
    //                                         and the buffer is a slice of that array, omitted slices
    //                                         could be either true or false signified by the initial
    //                                         value returned.
}

/// Iterate over an array of primitives by dispatching at run-time on the array type.
#[macro_export]
macro_rules! iterate_primitive_array {
    ($self:expr, | $_1:tt $rust_type:ident, $_2:tt $iterator:ident | $($body:tt)*) => ({
        macro_rules! __with__ {( $_1:tt $rust_type:ident, $_2:tt $iterator:ident ) => ( $($body)* )}
        use vortex_error::VortexExpect;
        match $self.ptype() {
            PType::I8 => __with__! { i8, $self.i8_iter().vortex_expect("i8 array must have i8_iter") },
            PType::I16 => __with__! { i16, $self.i16_iter().vortex_expect("i16 array must have i16_iter") },
            PType::I32 => __with__! { i32, $self.i32_iter().vortex_expect("i32 array must have i32_iter") },
            PType::I64 => __with__! { i64, $self.i64_iter().vortex_expect("i64 array must have i64_iter") },
            PType::U8 => __with__! { u8, $self.u8_iter().vortex_expect("u8 array must have u8_iter") },
            PType::U16 => __with__! { u16, $self.u16_iter().vortex_expect("u16 array must have u16_iter") },
            PType::U32 => __with__! { u32, $self.u32_iter().vortex_expect("u32 array must have u32_iter") },
            PType::U64 => __with__! { u64, $self.u64_iter().vortex_expect("u64 array must have u64_iter") },
            PType::F16 => __with__! { f16, $self.f16_iter().vortex_expect("f16 array must have f16_iter") },
            PType::F32 => __with__! { f32, $self.f32_iter().vortex_expect("f32 array must have f32_iter") },
            PType::F64 => __with__! { f64, $self.f64_iter().vortex_expect("f64 array must have f64_iter") },
        }
    })
}

/// Iterate over an array of integers by dispatching at run-time on the array type.
#[macro_export]
macro_rules! iterate_integer_array {
    ($self:expr, | $_1:tt $rust_type:ident, $_2:tt $iterator:ident | $($body:tt)*) => ({
        macro_rules! __with__ {( $_1 $rust_type:ident, $_2 $iterator:expr ) => ( $($body)* )}
        use vortex_error::VortexExpect;
        match $self.ptype() {
            PType::I8 => __with__! { i8, $self.i8_iter().vortex_expect("i8 array must have i8_iter") },
            PType::I16 => __with__! { i16, $self.i16_iter().vortex_expect("i16 array must have i16_iter") },
            PType::I32 => __with__! { i32, $self.i32_iter().vortex_expect("i32 array must have i32_iter") },
            PType::I64 => __with__! { i64, $self.i64_iter().vortex_expect("i64 array must have i64_iter") },
            PType::U8 => __with__! { u8, $self.u8_iter().vortex_expect("u8 array must have u8_iter") },
            PType::U16 => __with__! { u16, $self.u16_iter().vortex_expect("u16 array must have u16_iter") },
            PType::U32 => __with__! { u32, $self.u32_iter().vortex_expect("u32 array must have u32_iter") },
            PType::U64 => __with__! { u64, $self.u64_iter().vortex_expect("u64 array must have u64_iter") },
            PType::F16 => panic!("unsupported type: f16"),
            PType::F32 => panic!("unsupported type: f32"),
            PType::F64 => panic!("unsupported type: f64"),
        }
    })
}

pub trait PrimitiveArrayTrait: ArrayTrait {
    fn ptype(&self) -> PType {
        if let DType::Primitive(ptype, ..) = self.dtype() {
            *ptype
        } else {
            vortex_panic!("array must have primitive data type");
        }
    }

    fn u8_accessor(&self) -> Option<AccessorRef<u8>> {
        None
    }

    fn u16_accessor(&self) -> Option<AccessorRef<u16>> {
        None
    }

    fn u32_accessor(&self) -> Option<AccessorRef<u32>> {
        None
    }

    fn u64_accessor(&self) -> Option<AccessorRef<u64>> {
        None
    }

    fn i8_accessor(&self) -> Option<AccessorRef<i8>> {
        None
    }

    fn i16_accessor(&self) -> Option<AccessorRef<i16>> {
        None
    }

    fn i32_accessor(&self) -> Option<AccessorRef<i32>> {
        None
    }

    fn i64_accessor(&self) -> Option<AccessorRef<i64>> {
        None
    }

    fn f16_accessor(&self) -> Option<AccessorRef<vortex_dtype::half::f16>> {
        None
    }

    fn f32_accessor(&self) -> Option<AccessorRef<f32>> {
        None
    }

    fn f64_accessor(&self) -> Option<AccessorRef<f64>> {
        None
    }

    fn u8_iter(&self) -> Option<VectorizedArrayIter<u8>> {
        self.u8_accessor().map(VectorizedArrayIter::new)
    }

    fn u16_iter(&self) -> Option<VectorizedArrayIter<u16>> {
        self.u16_accessor().map(VectorizedArrayIter::new)
    }

    fn u32_iter(&self) -> Option<VectorizedArrayIter<u32>> {
        self.u32_accessor().map(VectorizedArrayIter::new)
    }

    fn u64_iter(&self) -> Option<VectorizedArrayIter<u64>> {
        self.u64_accessor().map(VectorizedArrayIter::new)
    }

    fn i8_iter(&self) -> Option<VectorizedArrayIter<i8>> {
        self.i8_accessor().map(VectorizedArrayIter::new)
    }

    fn i16_iter(&self) -> Option<VectorizedArrayIter<i16>> {
        self.i16_accessor().map(VectorizedArrayIter::new)
    }

    fn i32_iter(&self) -> Option<VectorizedArrayIter<i32>> {
        self.i32_accessor().map(VectorizedArrayIter::new)
    }

    fn i64_iter(&self) -> Option<VectorizedArrayIter<i64>> {
        self.i64_accessor().map(VectorizedArrayIter::new)
    }

    fn f16_iter(&self) -> Option<VectorizedArrayIter<vortex_dtype::half::f16>> {
        self.f16_accessor().map(VectorizedArrayIter::new)
    }

    fn f32_iter(&self) -> Option<VectorizedArrayIter<f32>> {
        self.f32_accessor().map(VectorizedArrayIter::new)
    }

    fn f64_iter(&self) -> Option<VectorizedArrayIter<f64>> {
        self.f64_accessor().map(VectorizedArrayIter::new)
    }
}

pub trait Utf8ArrayTrait: ArrayTrait {}

pub trait BinaryArrayTrait: ArrayTrait {}

pub trait StructArrayTrait: ArrayTrait {
    fn names(&self) -> &FieldNames {
        let DType::Struct(st, _) = self.dtype() else {
            unreachable!()
        };
        st.names()
    }

    fn dtypes(&self) -> &[DType] {
        let DType::Struct(st, _) = self.dtype() else {
            unreachable!()
        };
        st.dtypes()
    }

    fn nfields(&self) -> usize {
        self.names().len()
    }

    /// Return a field's array by index
    fn field(&self, idx: usize) -> Option<ArrayData>;

    /// Return a field's array by name
    fn field_by_name(&self, name: &str) -> Option<ArrayData> {
        let field_idx = self
            .names()
            .iter()
            .position(|field_name| field_name.as_ref() == name);

        field_idx.and_then(|field_idx| self.field(field_idx))
    }

    fn project(&self, projection: &[Field]) -> VortexResult<ArrayData>;
}

pub trait ListArrayTrait: ArrayTrait {}

pub trait ExtensionArrayTrait: ArrayTrait {
    /// Returns the extension logical [`DType`].
    fn ext_dtype(&self) -> &Arc<ExtDType> {
        let DType::Extension(ext_dtype) = self.dtype() else {
            vortex_panic!("Expected ExtDType")
        };
        ext_dtype
    }

    /// Returns the underlying [`ArrayData`], without the [`ExtDType`].
    fn storage_data(&self) -> ArrayData;
}
