// Copyright 2023 The Abseil Authors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#ifndef ABSL_LOG_INTERNAL_FNMATCH_H_
#define ABSL_LOG_INTERNAL_FNMATCH_H_

#include "absl/base/config.h"
#include "absl/strings/string_view.h"

namespace absl {
ABSL_NAMESPACE_BEGIN
namespace log_internal {
// Like POSIX `fnmatch`, but:
// * accepts `string_view`
// * does not allocate any dynamic memory
// * only supports * and ? wildcards and not bracket expressions [...]
// * wildcards may match /
// * no backslash-escaping
bool FNMatch(absl::string_view pattern, absl::string_view str);
}  // namespace log_internal
ABSL_NAMESPACE_END
}  // namespace absl

#endif  // ABSL_LOG_INTERNAL_FNMATCH_H_
