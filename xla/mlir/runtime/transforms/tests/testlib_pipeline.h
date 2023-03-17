/* Copyright 2022 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

#ifndef XLA_MLIR_RUNTIME_TRANSFORMS_TESTS_TESTLIB_PIPELINE_H_
#define XLA_MLIR_RUNTIME_TRANSFORMS_TESTS_TESTLIB_PIPELINE_H_

#include "xla/runtime/compiler.h"

namespace xla {
namespace runtime {

// Registers dialects supported by the Xla runtime tests.
void RegisterXlaRuntimeTestlibDialects(DialectRegistry& dialects);

// Populates passes for compiling Xla runtime tests.
void CreateXlaRuntimeTestlibPipeline(PassManager& passes);

}  // namespace runtime
}  // namespace xla

#endif  // XLA_MLIR_RUNTIME_TRANSFORMS_TESTS_TESTLIB_PIPELINE_H_
