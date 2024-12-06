/*
 * Copyright 2024-2024 NVIDIA CORPORATION & AFFILIATES.  All rights reserved.
 *
 * NOTICE TO LICENSEE:
 *
 * This source code and/or documentation ("Licensed Deliverables") are
 * subject to NVIDIA intellectual property rights under U.S. and
 * international Copyright laws.
 *
 * These Licensed Deliverables contained herein is PROPRIETARY and
 * CONFIDENTIAL to NVIDIA and is being provided under the terms and
 * conditions of a form of NVIDIA software license agreement by and
 * between NVIDIA and Licensee ("License Agreement") or electronically
 * accepted by Licensee.  Notwithstanding any terms or conditions to
 * the contrary in the License Agreement, reproduction or disclosure
 * of the Licensed Deliverables to any third party without the express
 * written consent of NVIDIA is prohibited.
 *
 * NOTWITHSTANDING ANY TERMS OR CONDITIONS TO THE CONTRARY IN THE
 * LICENSE AGREEMENT, NVIDIA MAKES NO REPRESENTATION ABOUT THE
 * SUITABILITY OF THESE LICENSED DELIVERABLES FOR ANY PURPOSE.  IT IS
 * PROVIDED "AS IS" WITHOUT EXPRESS OR IMPLIED WARRANTY OF ANY KIND.
 * NVIDIA DISCLAIMS ALL WARRANTIES WITH REGARD TO THESE LICENSED
 * DELIVERABLES, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY,
 * NONINFRINGEMENT, AND FITNESS FOR A PARTICULAR PURPOSE.
 * NOTWITHSTANDING ANY TERMS OR CONDITIONS TO THE CONTRARY IN THE
 * LICENSE AGREEMENT, IN NO EVENT SHALL NVIDIA BE LIABLE FOR ANY
 * SPECIAL, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, OR ANY
 * DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
 * WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
 * ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
 * OF THESE LICENSED DELIVERABLES.
 *
 * U.S. Government End Users.  These Licensed Deliverables are a
 * "commercial item" as that term is defined at 48 C.F.R. 2.101 (OCT
 * 1995), consisting of "commercial computer software" and "commercial
 * computer software documentation" as such terms are used in 48
 * C.F.R. 12.212 (SEPT 1995) and is provided to the U.S. Government
 * only as a commercial end item.  Consistent with 48 C.F.R.12.212 and
 * 48 C.F.R. 227.7202-1 through 227.7202-4 (JUNE 1995), all
 * U.S. Government End Users acquire the Licensed Deliverables with
 * only those rights set forth herein.
 *
 * Any use of the Licensed Deliverables in individual and commercial
 * software must include, in the user documentation and internal
 * comments to the code, the above Disclaimer and U.S. Government End
 * Users Notice.
 * </blockquote>}
 */

/**
 * @file
 * \brief This file contains all public declarations of the cuDensityMat library.
 */

#pragma once

#include <library_types.h>    // CUDA data types
#include <cuComplex.h>        // CUDA complex numbers
#include <cuda_runtime_api.h> // CUDA runtime API
#include <stdint.h>           // C integer types

// LIBRARY VERSION

#define CUDENSITYMAT_MAJOR 0 //!< cuDensityMat major version.
#define CUDENSITYMAT_MINOR 0 //!< cuDensityMat minor version.
#define CUDENSITYMAT_PATCH 5 //!< cuDensityMat patch version.
#define CUDENSITYMAT_VERSION (CUDENSITYMAT_MAJOR * 10000 + CUDENSITYMAT_MINOR * 100 + CUDENSITYMAT_PATCH)


// MACRO CONSTANTS

/**
 * \brief The maximal length of the name for a user-provided memory pool.
 */
#define CUDENSITYMAT_ALLOCATOR_NAME_LEN 64


#if defined(__cplusplus)
#include <cstdint>
#include <cstdio>

extern "C" {
#else
#include <stdint.h>
#include <stdio.h>

#endif // defined(__cplusplus)


// CONSTANTS AND ENUMERATIONS

/**
 * \defgroup constenums Constants and Enumerations
 * \{
 */

/**
 * \brief Return status of the library API functions.
 *
 * \details All library API functions return a status
 * which can take one of the following values.
 */
typedef enum
{
  /** The operation has completed successfully. */
  CUDENSITYMAT_STATUS_SUCCESS                   = 0,
  /** The library is not initialized. */
  CUDENSITYMAT_STATUS_NOT_INITIALIZED           = 1,
  /** Resource allocation failed inside the library. */
  CUDENSITYMAT_STATUS_ALLOC_FAILED              = 3,
  /** An invalid parameter value was passed to a function (normally indicates a user error). */
  CUDENSITYMAT_STATUS_INVALID_VALUE             = 7,
  /** The GPU device is either not ready or the target architecture is not supported. */
  CUDENSITYMAT_STATUS_ARCH_MISMATCH             = 8,
  /** The GPU program failed to execute. This is often caused by a CUDA kernel launch failure on the GPU. */
  CUDENSITYMAT_STATUS_EXECUTION_FAILED          = 13,
  /** An internal library error has occurred. */
  CUDENSITYMAT_STATUS_INTERNAL_ERROR            = 14,
  /** The requested operation is not supported. */
  CUDENSITYMAT_STATUS_NOT_SUPPORTED             = 15,
  /** An error occurred inside a user callback function. */
  CUDENSITYMAT_STATUS_CALLBACK_ERROR            = 16,
  /** A call to the cuBLAS library did not succeed. */
  CUDENSITYMAT_STATUS_CUBLAS_ERROR              = 17,
  /** An unknown CUDA error has occurred. */
  CUDENSITYMAT_STATUS_CUDA_ERROR                = 18,
  /** The provided workspace buffer is insufficient. */
  CUDENSITYMAT_STATUS_INSUFFICIENT_WORKSPACE    = 19,
  /** The CUDA driver version is insufficient. */
  CUDENSITYMAT_STATUS_INSUFFICIENT_DRIVER       = 20,
  /** An error occurred during file I/O. */
  CUDENSITYMAT_STATUS_IO_ERROR                  = 21,
  /** The dynamically linked cuTENSOR library is incompatible. */
  CUDENSITYMAT_STATUS_CUTENSOR_VERSION_MISMATCH = 22,
  /** Drawing GPU device memory from a memory pool is requested, but the memory pool has not been set. */
  CUDENSITYMAT_STATUS_NO_DEVICE_ALLOCATOR       = 23,
  /** A call to the cuTENSOR library did not succeed. */
  CUDENSITYMAT_STATUS_CUTENSOR_ERROR            = 24,
  /** A call to the cuSOLVER library did not succeed. */
  CUDENSITYMAT_STATUS_CUDMLVER_ERROR            = 25,
  /** GPU device memory pool operation failure. */
  CUDENSITYMAT_STATUS_DEVICE_ALLOCATOR_ERROR    = 26,
  /** Distributed communication service failure. */
  CUDENSITYMAT_STATUS_DISTRIBUTED_FAILURE       = 27,
  /** Operation interrupted by the user and cannot recover or complete. */
  CUDENSITYMAT_STATUS_INTERRUPTED               = 28,
  /** A call to the cuTensorNet library did not succeed. */
  CUDENSITYMAT_STATUS_CUTENSORNET_ERROR         = 29
} cudensitymatStatus_t;

/**
 * @brief Supported compute types.
*/
typedef enum
{
  CUDENSITYMAT_COMPUTE_64F = (1U << 4U),
  CUDENSITYMAT_COMPUTE_32F = (1U << 2U)
} cudensitymatComputeType_t;

/**
 * \brief Supported providers of the distributed communication service.
 */
typedef enum
{
  CUDENSITYMAT_DISTRIBUTED_PROVIDER_NONE    = 0,  ///< No communication service provider (single-GPU execution)
  CUDENSITYMAT_DISTRIBUTED_PROVIDER_MPI     = 1,  ///< MPI communication service
  CUDENSITYMAT_DISTRIBUTED_PROVIDER_NCCL    = 2,  ///< NCCL communication service (may require MPI as well)
  CUDENSITYMAT_DISTRIBUTED_PROVIDER_NVSHMEM = 3   ///< NVSHMEM communication service
} cudensitymatDistributedProvider_t;

/**
 * \brief Quantum state purity (pure or mixed state).
 */
typedef enum
{
  CUDENSITYMAT_STATE_PURITY_PURE,   ///< Pure quantum state
  CUDENSITYMAT_STATE_PURITY_MIXED   ///< Mixed quantum state
} cudensitymatStatePurity_t;

/**
 * \brief Elementary operator sparsity kind.
 */
typedef enum
{
  CUDENSITYMAT_OPERATOR_SPARSITY_NONE          = 0,  ///< No sparsity (dense tensor)
  CUDENSITYMAT_OPERATOR_SPARSITY_MULTIDIAGONAL = 1   ///< Multi-diagonal sparsity (one or multiple diagonals)
} cudensitymatElementaryOperatorSparsity_t;


/**
 * \brief Memory spaces for workspace buffer allocation.
 */
typedef enum
{
  CUDENSITYMAT_MEMSPACE_DEVICE = 0, ///< Device memory space
  CUDENSITYMAT_MEMSPACE_HOST   = 1  ///< Host memory space
} cudensitymatMemspace_t;

/**
 * \brief Kinds of workspace buffers.
 */
typedef enum
{
  CUDENSITYMAT_WORKSPACE_SCRATCH = 0, ///< Scratch workspace memory
//CUDENSITYMAT_WORKSPACE_CACHE   = 1  ///< Cache workspace memory (must stay valid with unmodified content until all referencing operations are completed)
} cudensitymatWorkspaceKind_t;

/** \} end constenums */


// TYPES AND STRUCTURES

/**
 * \defgroup typestructs Types and Data Structures
 * \{
 */

/**
 * \brief Opaque data structure holding the library context (context handle).
 *
 * \details This handle holds the library context (device properties, system information, etc.).
 * The handle must be initialized and destroyed using the cudensitymatCreate() and cudensitymatDestroy()
 * functions, respectively.
 */
typedef void * cudensitymatHandle_t;

/**
 * \brief Opaque data structure holding the quantum state representation.
 *
 * \details The quantum state is defined by its purity (pure or mixed),
 * shape (specification of all quantum degrees of freedom), numerical
 * representation (tensor or matrix), structural compression (tensor network
 * or eigen decomposition), explicit symmetries (if any), etc.
 *
 * \note Each quantum degree of freedom is represented by a vector space
 * of some dimension. The full quantum state lives in a tensor product space
 * constructed from the vector spaces associated with the quantum degrees of freedom.
 * Additionally, a projected quantum state can be introduced by projecting
 * the full quantum state space to a lower-dimensional subspace.
 */
typedef void * cudensitymatState_t;

/**
 * \brief Opaque data structure representing an elementary tensor operator
 * acting on a single or multiple quantum degrees of freedom.
 */
typedef void * cudensitymatElementaryOperator_t;

/**
 * \brief Opaque data structure representing an operator term that can act
 * on a single or multiple quantum degrees of freedom from either side
 * of the mixed quantum state, i.e., either from the ket side or from
 * the bra side. For pure quantum states, it can only act from one side.
 *
 * \details Generally, an operator term is defined as a sum of products
 * of individual tensor operators, where each individual tensor operator
 * within a product acts on disjoint quantum degrees of freedom. The sum
 * may contain one or more such products, where each product may consist
 * of one or more tensor operators.
 */
typedef void * cudensitymatOperatorTerm_t;

/**
 * \brief Opaque data structure representing a composite operator (collection of operator terms)
 * that can act on a single or multiple degrees of freedom from either side of the mixed
 * quantum state, i.e., either from the ket side or from the bra side. For pure quantum states,
 * it can only act from one side.
 *
 * \details Here the operator is defined as a collection of one or more operator terms.
 */
typedef void * cudensitymatOperator_t;

/**
 * \brief Opaque data structure representing a collective action of a given number of operators
 * on the corresponding number of input quantum states, producing an update on a single
 * output quantum state (when the actual computation is performed).
 *
 * \details This data structure allows specification of a collective operator action
 * where both the operators and the input quantum states may be different in each
 * action pair. The action pair is defined as an operator acting on an input quantum state,
 * producing an update on the same output quantum state for each action pair.
 */
typedef void * cudensitymatOperatorAction_t;

/**
 * \brief Opaque data structure specifying the operator expectation value computation.
 *
 * \details This data structure encapsulates the given operator for which it will
 * be able to compute the expectation value over a given quantum state.
 */
typedef void * cudensitymatExpectation_t;

/**
 * \brief Opaque data structure describing a workspace buffer.
 */
typedef void * cudensitymatWorkspaceDescriptor_t;

/**
 * \brief Explicit data structure specifying a given time interval or time range.
 *
 * \details The time interval bounds are specified by two doubles,
 * timeStart and timeFinish. The explicit time range, that is, the
 * sequence of time points within the requested time interval can be
 * generated by either setting a time step or providing explicit
 * time points manually via a C array of doubles.
 *
 * \note Providing explicit time points (numPoints > 0)
 * overrides the timeStep value.
 */
typedef struct
{
  double timeStart;       ///< Start time
  double timeFinish;      ///< Finish time
  double timeStep;        ///< Time step (zero means undefined)
  int64_t numPoints;      ///< (Optional) Number of explicit time points inside the [timeStart:timeFinish] interval, 0 otherwise
  const double * points;  ///< (Optional) Ordered array with explicit time points inside the [timeStart:timeFinish] interval, NULL otherwise
} cudensitymatTimeRange_t;

/**
 * \brief Explicit data structure for storing an MPI communicator in a type-erased form.
 */
typedef struct {
  void * commPtr;  ///< owning pointer to the MPI_Comm data structure
  size_t commSize; ///< size of the MPI_Comm data structure
} cudensitymatDistributedCommunicator_t;

/**
 * \brief Opaque data structure storing a distributed communication request.
 */
typedef void * cudensitymatDistributedRequest_t;

/** \} end typestructs */


// USER-DEFINED FUNCTION SIGNATURES

/**
 * \brief External callback function returning a scalar.
 *
 * \details An external user-provided scalar callback function can be
 * registered with the library for deferred invocation at a given point
 * of time, supplied with some given real parameter values.
 *
 * \param[in] time Time value.
 * \param[in] numParams Number of external real parameters.
 * \param[in] params Array of the real parameter values.
 * \param[in] dataType Data type of the returned scalar.
 * \param[inout] scalarStorage Pointer to the scalar storage in CPU-accessible memory.
 * \return int32_t Error code.
 */
typedef int32_t (*cudensitymatScalarCallback_t) (double time,
                                              int32_t numParams,
                                              const double params[],
                                              cudaDataType_t dataType,
                                              void * scalarStorage);

/**
 * \brief External callback function returning a tensor.
 *
 * \details An external user-defined tensor callback function can be
 * registered with the library for deferred invocation at a given point
 * of time, supplied with some given real parameter values.
 *
 * \note A tensor callback function fills in a dense array
 * which represents an elementary tensor operator with its
 * specific sparsity kind:
 *  - CUDENSITYMAT_OPERATOR_SPARSITY_NONE:
 *      The returned dense array has exactly the same shape
 *      as the elementary tensor operator itself;
 *  - CUDENSITYMAT_OPERATOR_SPARSITY_MULTIDIAGONAL:
 *      The returned dense array has shape [N,M],
 *      where N is the dimension of the matrix of the elementary tensor operator,
 *      while M is the number of non-zero diagonals of that matrix,
 *      padded with trailing zeros to the full matrix dimension.
 *
 * \param[in] sparsity Elementary tensor operator sparsity kind.
 * \param[in] numModes Number of modes in the returned data array.
 * \param[in] modeExtents Mode extents in the returned data array.
 * \param[in] diagonalOffsets For CUDENSITYMAT_OPERATOR_SPARSITY_MULTIDIAGONAL,
 * offsets of the stored non-zero diagonals of the elementary tensor operator
 * matrix: The main diagonal has offset zero, the below-main diagonals have
 * negative offsets, the above-main diagonals have positive offsets.
 * For CUDENSITYMAT_OPERATOR_SPARSITY_NONE, this argument has no meaning
 * and can be set to NULL.
 * \param[in] time Time value.
 * \param[in] numParams Number of external real parameters.
 * \param[in] params Array of the real parameter values.
 * \param[in] dataType Data type of the returned array.
 * \param[inout] tensorStorage Pointer to the tensor elements storage (array data)
 * in CPU-accessible memory.
 * \return int32_t Error code.
 */
typedef int32_t (*cudensitymatTensorCallback_t) (cudensitymatElementaryOperatorSparsity_t sparsity,
                                              int32_t numModes,
                                              const int64_t modeExtents[],
                                              const int32_t diagonalOffsets[],
                                              double time,
                                              int32_t numParams,
                                              const double params[],
                                              cudaDataType_t dataType,
                                              void * tensorStorage);

/** Callback wrapper structs. */
typedef struct
{
  cudensitymatScalarCallback_t callback;
  void * wrapper;
} cudensitymatWrappedScalarCallback_t;

typedef struct
{
  cudensitymatTensorCallback_t callback;
  void * wrapper;
} cudensitymatWrappedTensorCallback_t;

/**
 * \typedef cudensitymatLoggerCallback_t
 * \brief A callback function pointer type for logging APIs. Use cudensitymatLoggerSetCallback() to set the callback function.
 * \param[in] logLevel the log level
 * \param[in] functionName the name of the API that logged this message
 * \param[in] message the log message
 */
typedef void (*cudensitymatLoggerCallback_t)(
    int32_t logLevel,
    const char *functionName,
    const char *message);

/**
 * \typedef cudensitymatLoggerCallbackData_t
 * \brief A callback function pointer type for logging APIs. Use cudensitymatLoggerSetCallbackData() to set the callback function and user data.
 * \param[in] logLevel the log level
 * \param[in] functionName the name of the API that logged this message
 * \param[in] message the log message
 * \param[in] userData user's data to be used by the callback
 */
typedef void (*cudensitymatLoggerCallbackData_t)(
    int32_t logLevel,
    const char *functionName,
    const char *message,
    void *userData);


// API FUNCTIONS

/**
 * \defgroup contextAPI Initialization and Management API
 * \{
 */

/**
 * \brief Creates and initializes the library context.
 * 
 * \param[out] handle Library handle.
 * \return cudensitymatStatus_t 
 */
cudensitymatStatus_t cudensitymatCreate(cudensitymatHandle_t * handle);

/**
 * \brief Destroys the library context.
 * 
 * \param[in] handle Library handle.
 * \return cudensitymatStatus_t 
 */
cudensitymatStatus_t cudensitymatDestroy(cudensitymatHandle_t handle);

/**
 * \brief Resets the current distributed execution configuration
 * associated with the given library context.
 *
 * \details Accepts and stores a copy of the provided communicator
 * which will be used for distributing numerical operations across
 * all involved distributed processes.
 *
 * \param[inout] handle Library handle.
 * \param[in] provider Communication service provider.
 * \param[in] commPtr Pointer to the communicator in a type-erased form.
 * \param[in] commSize Size of the communicator in bytes.
 * \return cudensitymatStatus_t 
 */
cudensitymatStatus_t cudensitymatResetDistributedConfiguration(
                    cudensitymatHandle_t handle,
                    cudensitymatDistributedProvider_t provider,
                    const void * commPtr,
                    size_t commSize);

/**
 * \brief Returns the total number of distributed processes
 * associated with the given library context.
 * 
 * \param[in] handle Library handle.
 * \param[out] numRanks Number of distributed processes.
 * \return cudensitymatStatus_t 
 */
cudensitymatStatus_t cudensitymatGetNumRanks(
                    const cudensitymatHandle_t handle,
                    int32_t * numRanks);

/**
 * \brief Returns the rank of the current process in the distributed
 * configuration associated with the given library context.
 * 
 * \param[in] handle Library handle.
 * \param[out] procRank Rank of the current distributed process.
 * \return cudensitymatStatus_t 
 */
cudensitymatStatus_t cudensitymatGetProcRank(
                    const cudensitymatHandle_t handle,
                    int32_t * procRank);

/**
 * \brief Resets the random seed used by the random number generator
 * inside the library context.
 * 
 * \param[inout] handle Library handle.
 * \param[in] randomSeed Random seed value.
 * \return cudensitymatStatus_t 
 */
cudensitymatStatus_t cudensitymatResetRandomSeed(
                    cudensitymatHandle_t handle,
                    int32_t randomSeed);

/** \} end contextAPI */

/**
 * \defgroup stateAPI Quantum State Definition API
 * \{
 */

/**
 * \brief Defines an empty quantum state of a given purity and shape,
 * or a batch of such quantum states.
 *
 * \details The number of space modes defining the state space is always the
 * number of quantum degrees of freedom used to define the corresponding
 * composite tensor-product space. With that, the number of modes in a
 * pure-state tensor equals the number of space modes (quantum degrees of freedom).
 * The number of modes in a mixed-state tensor equals twice the number of the space modes,
 * consisting of a set of the ket modes and the bra modes, which are identical in terms
 * of their extents between the two sets, and the ket modes precede the bra modes, for example:
 * S[i0, i1, j0, j1] tensor represents a mixed quantum state with two degree of freedom,
 * where modes {i0, i1} form the ket set, and modes {j0, j1} form the bra set such that
 * ket mode i0 corresponds to the bra mode j0, and ket mode i1 corresponds to the bra mode j1.
 * In contrast, a pure quantum state with two degrees of freedom is represented by the tensor
 * S[i0, i1] with only ket modes (no bra modes). Furthermore, batched pure/mixed states
 * add one additional (batch) mode to their dense tensor representation, namely:
 * S[i0, i1, b] for the pure state, and S[i0, i1, j0, j1, b] for the mixed state,
 * where b is the size of the batch (batch dimension).
 *
 * \param[in] handle Library handle.
 * \param[in] purity Desired quantum state purity.
 * \param[in] numSpaceModes Number of space modes (number of degrees of freedom).
 * \param[in] spaceModeExtents Extents of the space modes (dimensions of the degrees of freedom).
 * \param[in] batchSize Batch size (number of equally-shaped quantum states).
 * Setting the batch size to zero is the same as setting it to 1.
 * \param[in] dataType Representation data type (type of tensor elements).
 * \param[out] state Empty quantum state (or a batch of quantum states).
 * \return cudensitymatStatus_t 
 */
cudensitymatStatus_t cudensitymatCreateState(
                    const cudensitymatHandle_t handle,
                    cudensitymatStatePurity_t purity,
                    int32_t numSpaceModes,
                    const int64_t spaceModeExtents[],
                    int64_t batchSize,
                    cudaDataType_t dataType,
                    cudensitymatState_t * state);

/**
 * \brief Destroys the quantum state.
 * 
 * \param[in] state Quantum state (or a batch of quantum states).
 * \return cudensitymatStatus_t 
 */
cudensitymatStatus_t cudensitymatDestroyState(cudensitymatState_t state);

/**
 * \brief Queries the number of components (tensors) constituting
 * the chosen quantum state representation (on the current process
 * in multi-process runs).
 *
 * \details Quantum state representation may include one or more
 * components (tensors) distributed over one or more parallel
 * processes (in distributed multi-GPU runs). The full state vector
 * or density matrix representations consist of only one component,
 * the full state tensor, which can be sliced and distributed over
 * all parallel processes (in distributed multi-GPU runs).
 * Factorized quantum state representations include more than one
 * component, and these components (tensors) are generally distributed
 * over all parallel processes (in distributed multi-GPU runs).
 *
 * \note In multi-process runs, this function returns the number
 * of locally stored components which, in general, can be smaller
 * than the total number of components stored across all parallel
 * processes. One can use the API function `cudensitymatStateGetComponentInfo`
 * to obtain more information on a given local component by providing
 * its local id.
 *
 * \note Batching does not add new components to the quantum state
 * representation, it just makes all existing components batched.
 * The corresponding tensors acquire one additional (most significant)
 * mode which represents the batch dimension.
 *
 * \param[in] handle Library handle.
 * \param[in] state Quantum state (or a batch of quantum states).
 * \param[out] numStateComponents Number of components (tensors)
 * in the quantum state representation (on the current process).
 * \return cudensitymatStatus_t 
 */
cudensitymatStatus_t cudensitymatStateGetNumComponents(
                    const cudensitymatHandle_t handle,
                    const cudensitymatState_t state,
                    int32_t * numStateComponents);

/**
 * \brief Queries the storage size (in bytes) for each
 * component (tensor) constituting the quantum state representation
 * (on the current process in multi-process runs).
 *
 * \param[in] handle Library handle.
 * \param[in] state Quantum state (or a batch of quantum states).
 * \param[in] numStateComponents Number of components (tensors)
 * in the quantum state representation (on the current process).
 * \param[out] componentSize Storage size (bytes) for each
 * component (tensor) consituting the quantum state representation
 * (on the current process).
 * \return cudensitymatStatus_t 
 */
cudensitymatStatus_t cudensitymatStateGetComponentStorageSize(
                    const cudensitymatHandle_t handle,
                    const cudensitymatState_t state,
                    int32_t numStateComponents,
                    size_t componentBufferSize[]);

/**
 * \brief Attaches a user-owned GPU-accessible storage buffer for each
 * component (tensor) constituting the quantum state representation
 * (on the current process in multi-process runs).
 *
 * \details The provided user-owned GPU-accessible storage buffers
 * will be used for storing components (tensors) constituting
 * the quantum state representation (on the current process
 * in multi-process runs). The initial value of the provided
 * storage buffers will be respected by the library,
 * thus providing a mechanism for specifing any initial value
 * of the quantum state in its chosen representation form.
 * In multi-process runs, the API function `cudensitymatGetComponentInfo`
 * will return the information which slice of the requested component
 * (tensor) is stored on the current process.
 *
 * \param[in] handle Library handle.
 * \param[inout] state Quantum state (or a batch of quantum states)
 * \param[in] numStateComponents Number of components (tensors)
 * in the quantum state representation (on the current process).
 * \param[in] componentBuffer Pointers to user-owned GPU-accessible
 * storage buffers for all components (tensors) constituting
 * the quantum state representation (on the current process).
 * \param[in] componentBufferSize Sizes of the provded storage
 * buffers for all components (tensors) constituting the quantum
 * state representation (on the current process).
 * \return cudensitymatStatus_t 
 *
 * \note The sizes of the provided storage buffers must be equal
 * or larger to the required sizes retrived via `cudensitymatStateGetComponentStorageSize`.
 */
cudensitymatStatus_t cudensitymatStateAttachComponentStorage(
                    const cudensitymatHandle_t handle,
                    cudensitymatState_t state,
                    int32_t numStateComponents,
                    void * componentBuffer[],
                    const size_t componentBufferSize[]);

/**
 * \brief Queries the number of modes in a local component tensor
 * (on the current process in multi-process runs).
 *
 * \param[in] handle Library handle.
 * \param[in] state Quantum state (or a batch of quantum states).
 * \param[in] stateComponentLocalId Component local id (on the current parallel process).
 * \param[out] stateComponentGlobalId Component global id (across all parallel processes).
 * \param[out] stateComponentNumModes Component tensor order (number of modes).
 * \param[out] batchModeLocation Location of the batch mode
 * (or -1 if the batch mode is absent).
 * \return cudensitymatStatus_t 
 */
cudensitymatStatus_t cudensitymatStateGetComponentNumModes(
                    const cudensitymatHandle_t handle,
                    cudensitymatState_t state,
                    int32_t stateComponentLocalId,
                    int32_t * stateComponentGlobalId,
                    int32_t * stateComponentNumModes,
                    int32_t * batchModeLocation);

/**
 * \brief Queries information for a locally stored component
 * tensor which represents either the full component or its slice
 * (on the current process in multi-process runs).
 *
 * \details This API function queries the global component id
 * (across all parallel processes), the number of tensor modes
 * (including the batch mode if present), the extents of all modes,
 * and the base offsets for all modes which can be different from
 * zero if the locally stored component tensor represents a slice
 * of the full component tensor. A base offset of a sliced mode is
 * the starting index value of that mode inside the full tensor mode.
 *
 * \param[in] handle Library handle.
 * \param[in] state Quantum state (or a batch of quantum states).
 * \param[in] stateComponentLocalId Component local id (on the current parallel process).
 * \param[out] stateComponentGlobalId Component global id (across all parallel processes).
 * \param[out] stateComponentNumModes Component tensor order (number of modes).
 * \param[out] stateComponentModeExtents Component tensor mode extents
 * (the size of the array must be sufficient, see `cudensitymatStateGetComponentNumModes`)
 * \param[out] stateComponentModeOffsets Component tensor mode offsets
 * (the size of the array must be sufficient, see `cudensitymatStateGetComponentNumModes`)
 * \return cudensitymatStatus_t 
 */
cudensitymatStatus_t cudensitymatStateGetComponentInfo(
                    const cudensitymatHandle_t handle,
                    cudensitymatState_t state,
                    int32_t stateComponentLocalId,
                    int32_t * stateComponentGlobalId,
                    int32_t * stateComponentNumModes,
                    int64_t stateComponentModeExtents[],
                    int64_t stateComponentModeOffsets[]);

/**
 * \brief Initializes the quantum state to zero (null state).
 * 
 * \param[in] handle Library handle.
 * \param[inout] state Quantum state (or a batch of quantum states).
 * \param[in] stream CUDA stream.
 * \return cudensitymatStatus_t 
 */
cudensitymatStatus_t cudensitymatStateInitializeZero(
                    const cudensitymatHandle_t handle,
                    cudensitymatState_t state,
                    cudaStream_t stream);

/**
 * \brief Initializes the quantum state to a random value.
 * 
 * \param[in] handle Library handle.
 * \param[inout] state Quantum state (or a batch of quantum states).
 * \param[in] stream CUDA stream.
 * \return cudensitymatStatus_t 
 */
/*cudensitymatStatus_t cudensitymatStateInitializeRandom(
                    const cudensitymatHandle_t handle,
                    cudensitymatState_t state,
                    cudaStream_t stream);
*/
/**
 * \brief Computes multiplication of the quantum state(s) by a scalar factor(s).
 *
 * \param[in] handle Library handle.
 * \param[inout] state Quantum state (or a batch of quantum states).
 * \param[in] scalingFactors Array of scaling factor(s) of dimension
 * equal to the batch size in the GPU-accessible RAM (same data type
 * as used by the state).
 * \param[in] stream CUDA stream.
 * \return cudensitymatStatus_t 
 */
cudensitymatStatus_t cudensitymatStateComputeScaling(
                    const cudensitymatHandle_t handle,
                    cudensitymatState_t state,
                    const void * scalingFactors,
                    cudaStream_t stream);

/**
 * \brief Computes the squared Frobenius norm(s) of the quantum state(s).
 *
 * \details The result is generally a vector of dimension
 * equal to the state batch size.
 *
 * \note For quantum states represented by complex data types,
 * the actual data type of the returned norm is float for cuFloatComplex
 * and double for cuDoubleComplex, respectively.
 *
 * \param[in] handle Library handle.
 * \param[in] state Quantum state (or a batch of quantum states).
 * \param[out] norm Pointer to the squared Frobenius norm(s) vector storage
 * in the GPU-accessible RAM (float or double real data type).
 * \param[in] stream CUDA stream.
 * \return cudensitymatStatus_t 
 *
 * \note For quantum states represented by FP32 complex numbers
 * the norm type is float; For quantum states represented by
 * FP64 complex numbers the norm type is double.
 */
cudensitymatStatus_t cudensitymatStateComputeNorm(
                    const cudensitymatHandle_t handle,
                    const cudensitymatState_t state,
                    void * norm,
                    cudaStream_t stream);

/**
 * \brief Computes the trace(s) of the quantum state(s).
 *
 * \details Trace of a pure state is defined to be its squared norm.
 * Trace of a mixed state is equal to the trace of its density matrix.
 * The result is generally a vector of dimension equal to the state batch size.
 *
 * \param[in] handle Library handle.
 * \param[in] state Quantum state (or a batch of quantum states).
 * \param[out] norm Pointer to the trace(s) vector storage
 * in the GPU-accessible RAM (same data type as used by the state).
 * \param[in] stream CUDA stream.
 * \return cudensitymatStatus_t 
 */
cudensitymatStatus_t cudensitymatStateComputeTrace(
                    const cudensitymatHandle_t handle,
                    const cudensitymatState_t state,
                    void * trace,
                    cudaStream_t stream);

/**
 * \brief Computes accumulation of a quantum state(s)
 * into another quantum state(s) of compatible shape.
 * 
 * \param[in] handle Library handle.
 * \param[in] stateIn Accumulated quantum state (or a batch of quantum states).
 * \param[inout] stateOut Accumulating quantum state (or a batch of quantum states).
 * \param[in] scalingFactors Array of scaling factor(s) of dimension
 * equal to the batch size in the GPU-accessible RAM (same data type
 * as used by the state).
 * \param[in] stream CUDA stream.
 * \return cudensitymatStatus_t 
 */
cudensitymatStatus_t cudensitymatStateComputeAccumulation(
                    const cudensitymatHandle_t handle,
                    const cudensitymatState_t stateIn,
                    cudensitymatState_t stateOut,
                    const void * scalingFactors,
                    cudaStream_t stream);

/**
 * \brief Computes the inner product(s) between the left quantum state(s)
 * and the right quantum state(s): < state(s)Left | state(s)Right >
 *
 * \details For pure quantum states, this function computes the regular
 * Hilbert-space inner product. For mixed quantum states, it computes
 * the matrix inner product induced by the Frobenius matrix norm:
 * The sum of regular Hilbert-space inner products for all columns
 * of two density matrices.
 *
 * \details The result is generally a vector of dimension
 * equal to the batch size of both states, which must be the same.
 * The participating quantum states must have compatible shapes.
 *
 * \param[in] handle Library handle.
 * \param[in] stateLeft Left quantum state (or a batch of quantum states).
 * \param[in] stateRight Right quantum state (or a batch of quantum states).
 * \param[out] innerProduct Pointer to the inner product(s) vector storage
 * in the GPU-accessible RAM (same data type as the one used by the quantum states).
 * \param[in] stream CUDA stream.
 * \return cudensitymatStatus_t 
 */
cudensitymatStatus_t cudensitymatStateComputeInnerProduct(
                    const cudensitymatHandle_t handle,
                    const cudensitymatState_t stateLeft,
                    const cudensitymatState_t stateRight,
                    void * innerProduct,
                    cudaStream_t stream);

/** \} end stateAPI */

/**
 * \defgroup operatorAPI Quantum Many-Body Operator API
 * \{
 */

/**
 * \brief Creates an elementary tensor operator acting on
 * a given number of quantum state modes (aka space modes).
 *
 * \details An elementary tensor operator is a single tensor operator
 * acting on a specific subset of space modes (quantum degrees of freedom).
 * The tensor operator is composed of a set of ket modes and a set of corresponding
 * bra modes of matching extents, where both sets have the same number of modes,
 * and the ket modes precede the bra modes, both in the same order. For example,
 * T[i0, i1, j0, j1] is a 2-body tensor operator in which modes {i0, i1} form
 * a set of ket modes while modes {j0, j1} form the corresponding set of bra modes,
 * where ket mode i0 corresponds to the bra mode j0, and ket mode i1 corresponds
 * to the bra mode j1 (the modes are always paired this way). Only one mode in each pair
 * of corresponding modes is contracted with the quantum state tensor, either from the left
 * or from the right. For example, either the bra mode j0 is contracted with a specific
 * ket mode of the quantum state, representing an operator action from the left,
 * or the ket mode i0 is contracted with a specific bra mode of the quantum state,
 * representing an operator action from the right. Then, the remaining uncontracted
 * mode replaces the contratcted mode of the quantum state.
 *
 * \details Storage of tensor elements in memory:
 * - CUDENSITYMAT_OPERATOR_SPARSITY_NONE:
 *   Dense tensor stored using the generalized column-wise layout.
 * - CUDENSITYMAT_OPERATOR_SPARSITY_MULTIDIAGONAL:
 *   The full non-zero diagonals are stored in a concatenated form
 *   following the order how they appear in the `diagonalOffsets` argument.
 *
 * \warning Different elementary tensor operators must not use the same
 * or overlapping GPU storage buffers, otherwise it will cause undefined behavior.
 *
 * \param[in] handle Library handle.
 * \param[in] numSpaceModes Number of the (state) space modes acted on.
 * \param[in] spaceModeExtents Extents of the (state) space modes acted on.
 * \param[in] sparsity Tensor operator sparsity defining the storage scheme.
 * \param[in] numDiagonals For multi-diagonal tensor operator matrices,
 * specifies the total number of non-zero diagonals.
 * \param[in] diagonalOffsets Offsets of the non-zero diagonals (for example,
 * the main diagonal has offset 0, the diagonal right above the main diagonal
 * has offset +1, the diagonal right below the main diagonal has offset -1, and so on).
 * \param[in] dataType Tensor operator data type.
 * \param[in] tensorData GPU-accessible pointer to the tensor operator elements storage.
 * \param[in] tensorCallback Optional user-defined tensor callback function
 * which can be called later to fill in the tensor elements in the provided storage, or NULL.
 * \param[out] elemOperator Elementary tensor operator.
 * \return cudensitymatStatus_t 
 */
cudensitymatStatus_t cudensitymatCreateElementaryOperator(
                    const cudensitymatHandle_t handle,
                    int32_t numSpaceModes,
                    const int64_t spaceModeExtents[],
                    cudensitymatElementaryOperatorSparsity_t sparsity,
                    int32_t numDiagonals,
                    const int32_t diagonalOffsets[],
                    cudaDataType_t dataType,
                    void * tensorData,
                    cudensitymatWrappedTensorCallback_t tensorCallback,
                    cudensitymatElementaryOperator_t * elemOperator);

/**
 * \brief Destroys an elementary tensor operator.
 * 
 * \param[in] elemOperator Elementary tensor operator.
 * \return cudensitymatStatus_t 
 */
cudensitymatStatus_t cudensitymatDestroyElementaryOperator(cudensitymatElementaryOperator_t elemOperator);

/**
 * \brief Creates an empty operator term which is going to be
 * a sum of tensor products of individual tensor operators,
 * where each individual tensor operator within a product acts on
 * disjoint quantum state modes (quantum degrees of freedom).
 *
 * \note The created operator term will only be able to act on the quantum states
 * which reside in the same space where the operator is set to act.
 * 
 * \param[in] handle Library handle.
 * \param[in] numSpaceModes Number of modes (degrees of freedom) defining
 * the primary/dual tensor product space in which the operator term will act.
 * \param[in] spaceModeExtents Extents of the modes (degrees of freedom) defining
 * the primary/dual tensor product space in which the operator term will act.
 * \param[out] operatorTerm Operator term.
 * \return cudensitymatStatus_t 
 */
cudensitymatStatus_t cudensitymatCreateOperatorTerm(
                    const cudensitymatHandle_t handle,
                    int32_t numSpaceModes,
                    const int64_t spaceModeExtents[],
                    cudensitymatOperatorTerm_t * operatorTerm);

/**
 * \brief Destroys an operator term.
 * 
 * \param[in] operatorTerm Operator term.
 * \return cudensitymatStatus_t 
 */
cudensitymatStatus_t cudensitymatDestroyOperatorTerm(cudensitymatOperatorTerm_t operatorTerm);

/**
 * \brief Appends a product of elementary tensor operators
 * acting on quantum state modes to the operator term.
 * 
 * \param[in] handle Library handle.
 * \param[inout] operatorTerm Operator term.
 * \param[in] numElemOperators Number of elementary tensor operators
 * in the tensor operator product.
 * \param[in] elemOperators Elementary tensor operators constituting
 * the tensor operator product.
 * \param[in] stateModesActedOn State modes acted on by the tensor operator product.
 * This is a concatenated list of the state modes acted on by all constituting elementary
 * tensor operators in the same order how they appear in the elemOperators argument.
 * \param[in] modeActionDuality Duality status of each mode action, that is,
 * whether the action applies to a ket mode of the quantum state (value 0)
 * or a bra mode of the quantum state (value 1 or other non-zero).
 * \param[in] coefficient Constant complex scalar coefficient associated
 * with the tensor operator product.
 * \param[in] coefficientCallback User-defined complex scalar callback function
 * which can be called later to update the scalar coefficient associated with
 * the tensor operator product, or NULL. The total coefficient associated with
 * the tensor operator product is a product of the constant coefficient and
 * the result of the scalar callback function, if defined.
 * \return cudensitymatStatus_t 
 */
cudensitymatStatus_t cudensitymatOperatorTermAppendElementaryProduct(
                    const cudensitymatHandle_t handle,
                    cudensitymatOperatorTerm_t operatorTerm,
                    int32_t numElemOperators,
                    const cudensitymatElementaryOperator_t elemOperators[],
                    const int32_t stateModesActedOn[],
                    const int32_t modeActionDuality[],
                    cuDoubleComplex coefficient,
                    cudensitymatWrappedScalarCallback_t coefficientCallback);

/**
 * \brief Appends a product of generic dense tensor operators
 * acting on different quantum state modes to the operator term.
 * 
 * \details This is a slightly more general version of `cudensitymatOperatorTermAppendElementaryProduct`
 * which does not require explicit construction of the `cudensitymatElementaryOperator_t` objects.
 * Additionally, it accepts specification of tensor storage strides when describing
 * the raw dense tensors representing tensor operators in the provided tensor operator product.
 * On the other hand, it does not allow specification of the tensor operator sparsity,
 * thus resulting in reduced performance for such cases.
 *
 * \warning Dense tensor operators from the appended tensor product
 * must not share GPU storage buffers. Each tensor operator appended
 * to the operator term as part of the tensor product via this API function
 * must have its own GPU storage buffer.
 *
 * \param[in] handle Library handle.
 * \param[inout] operatorTerm Operator term.
 * \param[in] numElemOperators Number of dense tensor operators in the given tensor operator product.
 * \param[in] numOperatorModes Number of modes in each tensor operator (twice the number of
 * state modes it acts on).
 * \param[in] operatorModeExtents Mode extents for each dense tensor operator.
 * \param[in] operatorModeStrides Mode strides for each dense tensor operator.
 * If a specific element is set to NULL, the corresponding dense tensor operator
 * will assume the default generalized column-wise storage strides.
 * \param[in] stateModesActedOn State modes acted on by the tensor operator product.
 * This is a concatenated list of the state modes acted on by all constituting dense
 * tensor operators in the same order how they appear in the above arguments.
 * \param[in] modeActionDuality Duality status of each mode action,
 * whether the action applies to a ket mode of the quantum state (value 0)
 * or a bra mode of the quantum state (value 1 or other non-zero).
 * \param[in] dataType Data type (for all dense tensor operators).
 * \param[in] tensorData GPU-accessible pointers to the elements of each dense
 * tensor operator constituting the tensor operator product.
 * \param[in] tensorCallbacks User-defined tensor callback functions which can be called
 * later to update the elements of each dense tensor operator (any of the callbacks can be NULL).
 * \param[in] coefficient Constant complex scalar coefficient associated with the tensor
 * operator product.
 * \param[in] coefficientCallback User-defined complex scalar callback function
 * which can be called later to update the scalar coefficient associated with
 * the tensor operator product, or NULL. The total coefficient associated with
 * the tensor operator product is a product of the constant coefficient and
 * the result of the scalar callback function, if defined.
 * \return cudensitymatStatus_t 
 */
cudensitymatStatus_t cudensitymatOperatorTermAppendGeneralProduct(
                    const cudensitymatHandle_t handle,
                    cudensitymatOperatorTerm_t operatorTerm,
                    int32_t numElemOperators,
                    const int32_t numOperatorModes[],
                    const int64_t * operatorModeExtents[],
                    const int64_t * operatorModeStrides[],
                    const int32_t stateModesActedOn[],
                    const int32_t modeActionDuality[],
                    cudaDataType_t dataType,
                    void * tensorData[],
                    cudensitymatWrappedTensorCallback_t tensorCallbacks[],
                    cuDoubleComplex coefficient,
                    cudensitymatWrappedScalarCallback_t coefficientCallback);

/**
 * \brief Creates an empty operator which is going to be
 * a collection of operator terms.
 *
 * \details If the operator is expected to act on a pure quantum state,
 * it is just a regular operator that will act on the pure state vector
 * from one side. If the operator is expected to act on a mixed quantum state,
 * its action can become more complicated where it may act on both sides
 * of the density matrix representing the mixed quantum state. In this case,
 * the operator is specifically called the super-operator. However, one
 * should note that in both cases this is still a mathematical operator,
 * just acting on a different kind of mathematical vector.
 *
 * \note The created operator will only be able to act on the quantum states
 * which reside in the same space where the operator is set to act.
 * 
 * \param[in] handle Library handle.
 * \param[in] numSpaceModes Number of modes (degrees of freedom) defining
 * the primary/dual tensor product space in which the operator term will act.
 * \param[in] spaceModeExtents Extents of the modes (degrees of freedom) defining
 * the primary/dual tensor product space in which the operator term will act.
 * \param[out] superoperator Operator.
 * \return cudensitymatStatus_t 
 */
cudensitymatStatus_t cudensitymatCreateOperator(
                    const cudensitymatHandle_t handle,
                    int32_t numSpaceModes,
                    const int64_t spaceModeExtents[],
                    cudensitymatOperator_t * superoperator);

/**
 * \brief Destroys an operator.
 * 
 * \param[in] superoperator Operator.
 * \return cudensitymatStatus_t 
 */
cudensitymatStatus_t cudensitymatDestroyOperator(cudensitymatOperator_t superoperator);

/**
 * \brief Appends an operator term to the operator.
 * 
 * \param[in] handle Library handle.
 * \param[inout] superoperator Operator.
 * \param[in] operatorTerm Operator term.
 * \param[in] duality Duality status of the operator term action as a whole.
 * If not zero, the duality status of each mode action inside the operator
 * term will be flipped, that is, action from the left will be replaced by
 * action from the right, and vice versa.
 * \param[in] coefficient Constant complex scalar coefficient associated with
 * the operator term.
 * \param[in] coefficientCallback User-defined complex scalar callback function
 * which can be called later to update the scalar coefficient associated with
 * the operator term, or NULL. The total coefficient associated with
 * the operator term is a product of the constant coefficient and
 * the result of the scalar callback function, if defined.
 * \return cudensitymatStatus_t 
 */
cudensitymatStatus_t cudensitymatOperatorAppendTerm(
                    const cudensitymatHandle_t handle,
                    cudensitymatOperator_t superoperator,
                    cudensitymatOperatorTerm_t operatorTerm,
                    int32_t duality,
                    cuDoubleComplex coefficient,
                    cudensitymatWrappedScalarCallback_t coefficientCallback);

/**
 * \brief Prepares the operator for an action on a quantum state.
 *
 * \details In general, before the operator action on a specific
 * quantum state(s) can be computed, it needs to be prepared
 * for computation first, which is the purpose of this API function.
 * 
 * \param[in] handle Library handle.
 * \param[in] superoperator Operator.
 * \param[in] stateIn Representative input quantum state on which the operator
 * is supposed to act. The actual state acted on during computation
 * may be different, but it has to be of the same shape, kind,
 * and factorization structure (topology, bond dimensions, etc).
 * \param[in] stateOut Representative output quantum state produced
 * by the action of the operator on the input quantum state. The actual state
 * acted on during computation may be different, but it has to be of the same shape,
 * kind, and factorization structure (topology, bond dimensions, etc).
 * \param[in] computeType Desired compute type.
 * \param[in] workspaceSizeLimit Workspace buffer size limit (bytes).
 * \param[inout] workspace Empty workspace descriptor on entrance.
 * The workspace size required for the computation will be set on exit.
 * \param[in] stream CUDA stream.
 * \return cudensitymatStatus_t 
 *
 * \note The required size of the workspace buffer returned inside
 * the workspace descriptor may sometimes be zero, in which case
 * there is no need to allocate a workspace buffer.
 */
cudensitymatStatus_t cudensitymatOperatorPrepareAction(
                    const cudensitymatHandle_t handle,
                    const cudensitymatOperator_t superoperator,
                    const cudensitymatState_t stateIn,
                    const cudensitymatState_t stateOut,
                    cudensitymatComputeType_t computeType,
                    size_t workspaceSizeLimit,
                    cudensitymatWorkspaceDescriptor_t workspace,
                    cudaStream_t stream);

/**
 * \brief Computes the action of the operator on a given input quantum state,
 * accumulating the result in the output quantum state (accumulative action).
 *
 * \note The provided input and output quantum states must be of the same
 * kind, shape, and structure as the quantum states provided during
 * the preceding preparation phase.
 * 
 * \param[in] handle Library handle.
 * \param[in] superoperator Operator.
 * \param[in] time Time value.
 * \param[in] numParams Number of variable parameters defined by the user.
 * \param[in] params Variable parameters defined by the user.
 * \param[in] stateIn Input quantum state (or a batch of input quantum states).
 * \param[inout] stateOut Updated resulting quantum state which
 * accumulates operator action on the input quantum state.
 * \param[in] workspace Allocated workspace descriptor.
 * \param[in] stream CUDA stream.
 * \return cudensitymatStatus_t 
 *
 * \warning The output quantum state cannot coincide with the input quantum state.
 */
cudensitymatStatus_t cudensitymatOperatorComputeAction(
                    const cudensitymatHandle_t handle,
                    const cudensitymatOperator_t superoperator,
                    double time,
                    int32_t numParams,
                    const double params[],
                    const cudensitymatState_t stateIn,
                    cudensitymatState_t stateOut,
                    cudensitymatWorkspaceDescriptor_t workspace,
                    cudaStream_t stream);

/**
 * \brief Creates an action descriptor for one or more operators,
 * thus defining an aggregate action of the operator(s) on a set
 * of input quantum states compliant with the operator domains,
 * where all input quantum states can also be batched.
 *
 * \details Specification of an operator itself is generally insufficient
 * for specifying the r.h.s. of the desired ordinary differential equation (ODE)
 * defining the evolution of the quantum state in time. In general,
 * the ODE r.h.s. specification requires specifying the action of one or more
 * operators on one or more (batched) quantum states (normally, density matrices).
 * The abstraction of the `OperatorAction` serves exactly this purpose.
 * When the aggregate operator action is computed, each provided operator
 * will act on its own input quantum state producing a contribution
 * to the same output quantum state.
 *
 * \note Sometimes one needs to solve a coupled system of ordinary
 * differential equations where a number of quantum states are
 * simultaneously evolved in time. In such a case, not all quantum
 * states have to affect the evolution of a given one of them.
 * To handle such cases, some of the operator-state products,
 * which do not contribute, can be set to zero by setting the
 * corresponding entry of the operators[] argument to NULL.
 * 
 * \param[in] handle Library handle.
 * \param[in] numOperators Number of operators involved (number of operator-state products).
 * \param[in] operators Constituting operator(s) with the same domain of action.
 * Some of the operators may be set to NULL to represent zero action on a specific
 * input quantum state.
 * \param[out] operatorAction Operator action.
 * \return cudensitymatStatus_t 
 */
cudensitymatStatus_t cudensitymatCreateOperatorAction(
                    const cudensitymatHandle_t handle,
                    int32_t numOperators,
                    cudensitymatOperator_t operators[],
                    cudensitymatOperatorAction_t * operatorAction);

/**
 * \brief Destroys the operator action descriptor.
 * 
 * \param[in] operatorAction Operator action.
 * \return cudensitymatStatus_t 
 */
cudensitymatStatus_t cudensitymatDestroyOperatorAction(cudensitymatOperatorAction_t operatorAction);

/**
 * \brief Prepares the (aggregate) operator(s) action for computation.
 *
 * \details In general, before the (aggregate) operator(s) action
 * on specific quantum states can be computed, it needs to be prepared
 * for computation first, which is the purpose of this API function.
 *
 * \param[in] handle Library handle.
 * \param[inout] operatorAction Operator(s) action specification.
 * \param[in] stateIn Input quantum state(s) for all operator(s)
 * defining the current Operator Action. Each input quantum state
 * can be a batch of quantum states itself (with the same batch dimension).
 * \param[in] stateOut Updated output quantum state (or a batch) which
 * accumulates the (aggregate) operator(s) action on all input quantum state(s).
 * \param[in] computeType Desired compute type.
 * \param[in] workspaceSizeLimit Workspace buffer size limit (bytes).
 * \param[inout] workspace Empty workspace descriptor on entrance.
 * The workspace size required for the computation will be set on exit.
 * \param[in] stream CUDA stream.
 * \return cudensitymatStatus_t 
 *
 * \note The required size of the workspace buffer returned inside
 * the workspace descriptor may sometimes be zero, in which case
 * there is no need to allocate a workspace buffer.
 */
cudensitymatStatus_t cudensitymatOperatorActionPrepare(
                    const cudensitymatHandle_t handle,
                    cudensitymatOperatorAction_t operatorAction,
                    const cudensitymatState_t stateIn[],
                    const cudensitymatState_t stateOut,
                    cudensitymatComputeType_t computeType,
                    size_t workspaceSizeLimit,
                    cudensitymatWorkspaceDescriptor_t workspace,
                    cudaStream_t stream);

/**
 * \brief Executes the action of one or more operators constituting
 * the aggreggate operator(s) action on the same number of input
 * quantum states, accumulating the results into a single output
 * quantum state.
 * 
 * \param[in] handle Library handle.
 * \param[inout] operatorAction Operator(s) action.
 * \param[in] time Time value.
 * \param[in] numParams Number of variable parameters defined by the user.
 * \param[in] params Variable parameters defined by the user.
 * \param[in] stateIn Input quantum state(s). Each input quantum state
 * can be a batch of quantum states, in general.
 * \param[inout] stateOut Updated output quantum state which
 * accumulates operator action(s) on all input quantum state(s).
 * \param[in] workspace Allocated workspace descriptor.
 * \param[in] stream CUDA stream.
 * \return cudensitymatStatus_t
 *
 * \note The output quantum state cannot be one of the input quantum states. 
 */
cudensitymatStatus_t cudensitymatOperatorActionCompute(
                    const cudensitymatHandle_t handle,
                    cudensitymatOperatorAction_t operatorAction,
                    double time,
                    int32_t numParams,
                    const double params[],
                    const cudensitymatState_t stateIn[],
                    cudensitymatState_t stateOut,
                    cudensitymatWorkspaceDescriptor_t workspace,
                    cudaStream_t stream);

/** \} end operatorAPI */

/**
 * \defgroup expectationAPI Expectation value API
 * \{
 */

/**
 * \brief Creates the operator expectation value computation object.
 *
 * \note The unnormalized expectation value will be produced
 * during the computation. If the quantum state is not normalized,
 * one will need to additionally compute the state norm or trace
 * in order to obtain the normalized operator expectation value.
 *
 * \param[in] handle Library handle.
 * \param[in] superoperator Operator.
 * \param[out] expectation Expectation value object.
 * \return cudensitymatStatus_t 
 * 
 * \note The operator must stay alive during the lifetime of the Expectation object.
 */
cudensitymatStatus_t cudensitymatCreateExpectation(
                    const cudensitymatHandle_t handle,
                    cudensitymatOperator_t superoperator,
                    cudensitymatExpectation_t * expectation);

/**
 * \brief Destroys an expectation value object.
 * 
 * \param[in] expectation Expectation value object.
 * \return cudensitymatStatus_t 
 */
cudensitymatStatus_t cudensitymatDestroyExpectation(cudensitymatExpectation_t expectation);

/**
 * \brief Prepares the expectation value object for computation.
 *
 * \details In general, before the expectation value can be computed,
 * it needs to be prepared for computation first, which is the purpose
 * of this API function.
 * 
 * \param[in] handle Library handle.
 * \param[inout] expectation Expectation value object.
 * \param[in] state Quantum state (or a batch of quantum states).
 * \param[in] computeType Desired compute type.
 * \param[in] workspaceSizeLimit Workspace buffer size limit (bytes).
 * \param[inout] workspace Empty workspace descriptor on entrance.
 * The workspace size required for the computation will be set on exit.
 * \param[in] stream CUDA stream.
 * \return cudensitymatStatus_t 
 *
 * \note The required size of the workspace buffer returned inside
 * the workspace descriptor may sometimes be zero, in which case
 * there is no need to allocate a workspace buffer.
 */
cudensitymatStatus_t cudensitymatExpectationPrepare(
                    const cudensitymatHandle_t handle,
                    cudensitymatExpectation_t expectation,
                    const cudensitymatState_t state,
                    cudensitymatComputeType_t computeType,
                    size_t workspaceSizeLimit,
                    cudensitymatWorkspaceDescriptor_t workspace,
                    cudaStream_t stream);

/**
 * \brief Computes the operator expectation value(s) with respect to the given quantum state(s).
 * 
 * \details The result is generally a vector of dimension equal to the state batch size.
 * 
 * \param[in] handle Library handle.
 * \param[in] expectation Expectation value object.
 * \param[in] time Specified time.
 * \param[in] numParams Number of variable parameters defined by the user.
 * \param[in] params Variable parameters defined by the user.
 * \param[in] state Quantum state (or a batch of quantum states).
 * \param[out] expectationValue Pointer to the expectation value(s) vector storage
 * in GPU-accessible RAM of the same data type as used by the state and operator.
 * \param[in] workspace Allocated workspace descriptor.
 * \param[in] stream CUDA stream.
 * \return cudensitymatStatus_t 
 */
cudensitymatStatus_t cudensitymatExpectationCompute(
                    const cudensitymatHandle_t handle,
                    cudensitymatExpectation_t expectation,
                    double time,
                    int32_t numParams,
                    const double params[],
                    const cudensitymatState_t state,
                    void * expectationValue,
                    cudensitymatWorkspaceDescriptor_t workspace,
                    cudaStream_t stream);

/** \} end expectationAPI */

/**
 * \defgroup workspaceAPI Workspace API
 * \{
 */

/**
 * \brief Creates a workspace descriptor.
 * 
 * \param[in] handle Library handle.
 * \param[out] workspaceDescr Workspace descriptor.
 * \return cudensitymatStatus_t 
 */
cudensitymatStatus_t cudensitymatCreateWorkspace(
                    const cudensitymatHandle_t handle,
                    cudensitymatWorkspaceDescriptor_t * workspaceDescr);

/**
 * \brief Destroys a workspace descriptor.
 * 
 * \param[inout] workspaceDescr Workspace descriptor.
 * \return cudensitymatStatus_t 
 */
cudensitymatStatus_t cudensitymatDestroyWorkspace(
                    cudensitymatWorkspaceDescriptor_t workspaceDescr);

/**
 * \brief Queries the required workspace buffer size.
 * 
 * \param[in] handle Library handle.
 * \param[in] workspaceDescr Workspace descriptor.
 * \param[in] memSpace Memory space.
 * \param[in] workspaceKind Workspace kind.
 * \param[out] memoryBufferSize Required workspace buffer size in bytes.
 * \return cudensitymatStatus_t 
 */
cudensitymatStatus_t cudensitymatWorkspaceGetMemorySize(
                    const cudensitymatHandle_t handle,
                    const cudensitymatWorkspaceDescriptor_t workspaceDescr,
                    cudensitymatMemspace_t memSpace,
                    cudensitymatWorkspaceKind_t workspaceKind,
                    size_t * memoryBufferSize);

/**
 * \brief Attaches memory to a workspace buffer.
 * 
 * \param[in] handle Library handle.
 * \param[inout] workspaceDescr Workspace descriptor.
 * \param[in] memSpace Memory space.
 * \param[in] workspaceKind Workspace kind.
 * \param[in] memoryBuffer Pointer to a user-owned memory buffer
 * to be used by the specified workspace.
 * \param[in] memoryBufferSize Size of the provided memory buffer in bytes.
 * \return cudensitymatStatus_t 
 */
cudensitymatStatus_t cudensitymatWorkspaceSetMemory(
                    const cudensitymatHandle_t handle,
                    cudensitymatWorkspaceDescriptor_t workspaceDescr,
                    cudensitymatMemspace_t memSpace,
                    cudensitymatWorkspaceKind_t workspaceKind,
                    void * memoryBuffer,
                    size_t memoryBufferSize);

/**
 * \brief Retrieves a workspace buffer.
 * 
 * \param[in] handle Library handle.
 * \param[in] workspaceDescr Workspace descriptor.
 * \param[in] memSpace Memory space.
 * \param[in] workspaceKind Workspace kind.
 * \param[out] memoryBuffer Pointer to a user-owned memory buffer
 * used by the specified workspace.
 * \param[out] memoryBufferSize Size of the memory buffer in bytes.
 * \return cudensitymatStatus_t 
 */
cudensitymatStatus_t cudensitymatWorkspaceGetMemory(
                    const cudensitymatHandle_t handle,
                    const cudensitymatWorkspaceDescriptor_t workspaceDescr,
                    cudensitymatMemspace_t memSpace,
                    cudensitymatWorkspaceKind_t workspaceKind,
                    void ** memoryBuffer,
                    size_t * memoryBufferSize);

/** \} end workspaceAPI */

/**
 * \defgroup loggerAPI Logger API
 * \{
 */

/**
 * \brief This function sets the logging callback routine.
 * \param[in] callback Pointer to a callback function. Check ::cudensitymatLoggerCallback_t.
 */
/*cudensitymatStatus_t cudensitymatLoggerSetCallback(cudensitymatLoggerCallback_t callback);*/

/**
 * \brief This function sets the logging callback routine, along with user data.
 * \param[in] callback Pointer to a callback function. Check ::cudensitymatLoggerCallbackData_t.
 * \param[in] userData Pointer to user-provided data to be used by the callback.
 */
/*cudensitymatStatus_t cudensitymatLoggerSetCallbackData(cudensitymatLoggerCallbackData_t callback,
                                                 void *userData);*/

/**
 * \brief This function sets the logging output file.
 * \param[in] file An open file with write permission.
 */
/*cudensitymatStatus_t cudensitymatLoggerSetFile(FILE *file);*/

/**
 * \brief This function opens a logging output file in the given path.
 * \param[in] logFile Path to the logging output file.
 */
/*cudensitymatStatus_t cudensitymatLoggerOpenFile(const char *logFile);*/

/**
 * \brief This function sets the value of the logging level.
 * \param[in] level Log level, should be one of the following:
 * Level| Summary           | Long Description
 * -----|-------------------|-----------------
 *  "0" | Off               | logging is disabled (default)
 *  "1" | Errors            | only errors will be logged
 *  "2" | Performance Trace | API calls that launch CUDA kernels will log their parameters and important information
 *  "3" | Performance Hints | hints that can potentially improve the application's performance
 *  "4" | Heuristics Trace  | provides general information about the library execution, may contain details about heuristic status
 *  "5" | API Trace         | API Trace - API calls will log their parameter and important information
 */
/*cudensitymatStatus_t cudensitymatLoggerSetLevel(int32_t level);*/

/**
 * \brief This function sets the value of the log mask.
 *
 * \param[in]  mask  Value of the logging mask.
 * Masks are defined as a combination (bitwise OR) of the following masks:
 * Level| Description       |
 * -----|-------------------|
 *  "0" | Off               |
 *  "1" | Errors            |
 *  "2" | Performance Trace |
 *  "4" | Performance Hints |
 *  "8" | Heuristics Trace  |
 *  "16"| API Trace         |
 *
 * Refer to cudensitymatLoggerSetLevel() for details.
 */
/*cudensitymatStatus_t cudensitymatLoggerSetMask(int32_t mask);*/

/**
 * \brief This function disables logging for the entire run.
 */
/*cudensitymatStatus_t cudensitymatLoggerForceDisable();*/

/** \} end loggerAPI */

/**
 * \defgroup distrBindings Distributed Interface Bindings
 * \{
 */

#define CUDENSITYMAT_DISTRIBUTED_INTERFACE_VERSION 241110

/**
 * \brief (Internal): Dynamic API wrapper runtime binding table for the distributed communication service.
*/
typedef struct {
  int version;
  int (*getNumRanks)(const cudensitymatDistributedCommunicator_t*, int32_t*);
  int (*getNumRanksShared)(const cudensitymatDistributedCommunicator_t*, int32_t*);
  int (*getProcRank)(const cudensitymatDistributedCommunicator_t*, int32_t*);
  int (*barrier)(const cudensitymatDistributedCommunicator_t*);
  int (*createRequest)(cudensitymatDistributedRequest_t*);
  int (*destroyRequest)(cudensitymatDistributedRequest_t);
  int (*waitRequest)(cudensitymatDistributedRequest_t);
  int (*testRequest)(cudensitymatDistributedRequest_t, int32_t*);
  int (*send)(const cudensitymatDistributedCommunicator_t*,
              const void*, int32_t, cudaDataType_t, int32_t, int32_t);
  int (*sendAsync)(const cudensitymatDistributedCommunicator_t*,
                   const void*, int32_t, cudaDataType_t, int32_t, int32_t,
                   cudensitymatDistributedRequest_t);
  int (*receive)(const cudensitymatDistributedCommunicator_t*,
                 void*, int32_t, cudaDataType_t, int32_t, int32_t);
  int (*receiveAsync)(const cudensitymatDistributedCommunicator_t*,
                      void*, int32_t, cudaDataType_t, int32_t, int32_t,
                      cudensitymatDistributedRequest_t);
  int (*bcast)(const cudensitymatDistributedCommunicator_t*,
               void*, int32_t, cudaDataType_t, int32_t);
  int (*allreduce)(const cudensitymatDistributedCommunicator_t*,
                   const void*, void*, int32_t, cudaDataType_t);
  int (*allreduceInPlace)(const cudensitymatDistributedCommunicator_t*,
                          void*, int32_t, cudaDataType_t);
  int (*allreduceInPlaceMin)(const cudensitymatDistributedCommunicator_t*,
                             void*, int32_t, cudaDataType_t);
  int (*allreduceDoubleIntMinloc)(const cudensitymatDistributedCommunicator_t*,
                                  const void*, void*);
  int (*allgather)(const cudensitymatDistributedCommunicator_t*,
                   const void*, void*, int32_t, cudaDataType_t);
} cudensitymatDistributedInterface_t;

/** \} end distrBindings */

#if defined(__cplusplus)
} // extern "C"
#endif // defined(__cplusplus)
