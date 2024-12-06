/*
 * Copyright 2023 NVIDIA Corporation.  All rights reserved.
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
 */

#pragma once

#include <cal.h>
#include <cublas_v2.h>
#include <inttypes.h>
#include <stdio.h>

#define CUBLASMP_VER_MAJOR 0
#define CUBLASMP_VER_MINOR 2
#define CUBLASMP_VER_PATCH 1
#define CUBLASMP_VERSION (CUBLASMP_VER_MAJOR * 1000 + CUBLASMP_VER_MINOR * 100 + CUBLASMP_VER_PATCH)

#ifdef __cplusplus
extern "C"
{
#endif

typedef enum
{
    CUBLASMP_GRID_LAYOUT_COL_MAJOR,
    CUBLASMP_GRID_LAYOUT_ROW_MAJOR
} cublasMpGridLayout_t;

struct cublasMpHandle;
typedef struct cublasMpHandle* cublasMpHandle_t;

struct cublasMpGrid;
typedef struct cublasMpGrid* cublasMpGrid_t;

struct cublasMpMatrixDescriptor;
typedef struct cublasMpMatrixDescriptor* cublasMpMatrixDescriptor_t;

cublasStatus_t cublasMpCreate(cublasMpHandle_t* handle, cudaStream_t stream);

cublasStatus_t cublasMpDestroy(cublasMpHandle_t handle);

cublasStatus_t cublasMpGetVersion(cublasMpHandle_t handle, int* version);

cublasStatus_t cublasMpSetMathMode(cublasMpHandle_t handle, cublasMath_t mode);

cublasStatus_t cublasMpGetMathMode(cublasMpHandle_t handle, cublasMath_t* mode);

cublasStatus_t cublasMpGridCreate(
    cublasMpHandle_t handle,
    int64_t nprow,
    int64_t npcol,
    cublasMpGridLayout_t layout,
    cal_comm_t comm,
    cublasMpGrid_t* grid);

cublasStatus_t cublasMpGridDestroy(cublasMpHandle_t handle, cublasMpGrid_t grid);

cublasStatus_t cublasMpMatrixDescriptorCreate(
    cublasMpHandle_t handle,
    int64_t m,
    int64_t n,
    int64_t mb,
    int64_t nb,
    int64_t rsrc,
    int64_t csrc,
    int64_t lld,
    cudaDataType_t type,
    cublasMpGrid_t grid,
    cublasMpMatrixDescriptor_t* desc);

cublasStatus_t cublasMpMatrixDescriptorDestroy(cublasMpHandle_t handle, cublasMpMatrixDescriptor_t desc);

cublasStatus_t cublasMpTrsm_bufferSize(
    cublasMpHandle_t handle,
    cublasSideMode_t side,
    cublasFillMode_t uplo,
    cublasOperation_t trans,
    cublasDiagType_t diag,
    int64_t m,
    int64_t n,
    const void* alpha,
    const void* a,
    int64_t ia,
    int64_t ja,
    cublasMpMatrixDescriptor_t descA,
    void* b,
    int64_t ib,
    int64_t jb,
    cublasMpMatrixDescriptor_t descB,
    cublasComputeType_t computeType,
    size_t* workspaceSizeInBytesOnDevice,
    size_t* workspaceSizeInBytesOnHost);

cublasStatus_t cublasMpTrsm(
    cublasMpHandle_t handle,
    cublasSideMode_t side,
    cublasFillMode_t uplo,
    cublasOperation_t trans,
    cublasDiagType_t diag,
    int64_t m,
    int64_t n,
    const void* alpha,
    const void* a,
    int64_t ia,
    int64_t ja,
    cublasMpMatrixDescriptor_t descA,
    void* b,
    int64_t ib,
    int64_t jb,
    cublasMpMatrixDescriptor_t descB,
    cublasComputeType_t computeType,
    void* d_work,
    size_t workspaceSizeInBytesOnDevice,
    void* h_work,
    size_t workspaceSizeInBytesOnHost);

cublasStatus_t cublasMpGemm_bufferSize(
    cublasMpHandle_t handle,
    cublasOperation_t transA,
    cublasOperation_t transB,
    int64_t m,
    int64_t n,
    int64_t k,
    const void* alpha,
    const void* a,
    int64_t ia,
    int64_t ja,
    cublasMpMatrixDescriptor_t descA,
    const void* b,
    int64_t ib,
    int64_t jb,
    cublasMpMatrixDescriptor_t descB,
    const void* beta,
    void* c,
    int64_t ic,
    int64_t jc,
    cublasMpMatrixDescriptor_t descC,
    cublasComputeType_t computeType,
    size_t* workspaceSizeInBytesOnDevice,
    size_t* workspaceSizeInBytesOnHost);

cublasStatus_t cublasMpGemm(
    cublasMpHandle_t handle,
    cublasOperation_t transA,
    cublasOperation_t transB,
    int64_t m,
    int64_t n,
    int64_t k,
    const void* alpha,
    const void* a,
    int64_t ia,
    int64_t ja,
    cublasMpMatrixDescriptor_t descA,
    const void* b,
    int64_t ib,
    int64_t jb,
    cublasMpMatrixDescriptor_t descB,
    const void* beta,
    void* c,
    int64_t ic,
    int64_t jc,
    cublasMpMatrixDescriptor_t descC,
    cublasComputeType_t computeType,
    void* d_work,
    size_t workspaceSizeInBytesOnDevice,
    void* h_work,
    size_t workspaceSizeInBytesOnHost);

cublasStatus_t cublasMpSyrk_bufferSize(
    cublasMpHandle_t handle,
    cublasFillMode_t uplo,
    cublasOperation_t trans,
    int64_t n,
    int64_t k,
    const void* alpha,
    const void* a,
    int64_t ia,
    int64_t ja,
    cublasMpMatrixDescriptor_t descA,
    const void* beta,
    void* c,
    int64_t ic,
    int64_t jc,
    cublasMpMatrixDescriptor_t descC,
    cublasComputeType_t computeType,
    size_t* workspaceSizeInBytesOnDevice,
    size_t* workspaceSizeInBytesOnHost);

cublasStatus_t cublasMpSyrk(
    cublasMpHandle_t handle,
    cublasFillMode_t uplo,
    cublasOperation_t trans,
    int64_t n,
    int64_t k,
    const void* alpha,
    const void* a,
    int64_t ia,
    int64_t ja,
    cublasMpMatrixDescriptor_t descA,
    const void* beta,
    void* c,
    int64_t ic,
    int64_t jc,
    cublasMpMatrixDescriptor_t descC,
    cublasComputeType_t computeType,
    void* d_work,
    size_t workspaceSizeInBytesOnDevice,
    void* h_work,
    size_t workspaceSizeInBytesOnHost);

int64_t cublasMpNumroc(int64_t n, int64_t nb, uint32_t iproc, uint32_t isrcproc, uint32_t nprocs);

cublasStatus_t cublasMpGemr2D_bufferSize(
    cublasMpHandle_t handle,
    int64_t m,
    int64_t n,
    const void* a,
    int64_t ia,
    int64_t ja,
    cublasMpMatrixDescriptor_t descA,
    void* b,
    int64_t ib,
    int64_t jb,
    cublasMpMatrixDescriptor_t descB,
    size_t* workspaceSizeInBytesOnDevice,
    size_t* workspaceSizeInBytesOnHost,
    cal_comm_t global_comm);

cublasStatus_t cublasMpGemr2D(
    cublasMpHandle_t handle,
    int64_t m,
    int64_t n,
    const void* a,
    int64_t ia,
    int64_t ja,
    cublasMpMatrixDescriptor_t descA,
    void* b,
    int64_t ib,
    int64_t jb,
    cublasMpMatrixDescriptor_t descB,
    void* d_work,
    size_t workspaceSizeInBytesOnDevice,
    void* h_work,
    size_t workspaceSizeInBytesOnHost,
    cal_comm_t global_comm);

cublasStatus_t cublasMpTrmr2D_bufferSize(
    cublasMpHandle_t handle,
    cublasFillMode_t uplo,
    cublasDiagType_t diag,
    int64_t m,
    int64_t n,
    const void* a,
    int64_t ia,
    int64_t ja,
    cublasMpMatrixDescriptor_t descA,
    void* b,
    int64_t ib,
    int64_t jb,
    cublasMpMatrixDescriptor_t descB,
    size_t* workspaceSizeInBytesOnDevice,
    size_t* workspaceSizeInBytesOnHost,
    cal_comm_t global_comm);

cublasStatus_t cublasMpTrmr2D(
    cublasMpHandle_t handle,
    cublasFillMode_t uplo,
    cublasDiagType_t diag,
    int64_t m,
    int64_t n,
    const void* a,
    int64_t ia,
    int64_t ja,
    cublasMpMatrixDescriptor_t descA,
    void* b,
    int64_t ib,
    int64_t jb,
    cublasMpMatrixDescriptor_t descB,
    void* d_work,
    size_t workspaceSizeInBytesOnDevice,
    void* h_work,
    size_t workspaceSizeInBytesOnHost,
    cal_comm_t global_comm);

cublasStatus_t cublasMpGeadd_bufferSize(
    cublasMpHandle_t handle,
    cublasOperation_t trans,
    int64_t m,
    int64_t n,
    const void* alpha,
    const void* a,
    int64_t ia,
    int64_t ja,
    cublasMpMatrixDescriptor_t descA,
    const void* beta,
    void* c,
    int64_t ic,
    int64_t jc,
    cublasMpMatrixDescriptor_t descC,
    size_t* workspaceSizeInBytesOnDevice,
    size_t* workspaceSizeInBytesOnHost);

cublasStatus_t cublasMpGeadd(
    cublasMpHandle_t handle,
    cublasOperation_t trans,
    int64_t m,
    int64_t n,
    const void* alpha,
    const void* a,
    int64_t ia,
    int64_t ja,
    cublasMpMatrixDescriptor_t descA,
    const void* beta,
    void* c,
    int64_t ic,
    int64_t jc,
    cublasMpMatrixDescriptor_t descC,
    void* d_work,
    size_t workspaceSizeInBytesOnDevice,
    void* h_work,
    size_t workspaceSizeInBytesOnHost);

cublasStatus_t cublasMpTradd_bufferSize(
    cublasMpHandle_t handle,
    cublasFillMode_t uplo,
    cublasOperation_t trans,
    int64_t m,
    int64_t n,
    const void* alpha,
    const void* a,
    int64_t ia,
    int64_t ja,
    cublasMpMatrixDescriptor_t descA,
    const void* beta,
    void* c,
    int64_t ic,
    int64_t jc,
    cublasMpMatrixDescriptor_t descC,
    size_t* workspaceSizeInBytesOnDevice,
    size_t* workspaceSizeInBytesOnHost);

cublasStatus_t cublasMpTradd(
    cublasMpHandle_t handle,
    cublasFillMode_t uplo,
    cublasOperation_t trans,
    int64_t m,
    int64_t n,
    const void* alpha,
    const void* a,
    int64_t ia,
    int64_t ja,
    cublasMpMatrixDescriptor_t descA,
    const void* beta,
    void* c,
    int64_t ic,
    int64_t jc,
    cublasMpMatrixDescriptor_t descC,
    void* d_work,
    size_t workspaceSizeInBytesOnDevice,
    void* h_work,
    size_t workspaceSizeInBytesOnHost);

typedef void (*cublasMpLoggerCallback_t)(int logLevel, const char* functionName, const char* message);

cublasStatus_t cublasMpLoggerSetCallback(cublasMpLoggerCallback_t callback);

cublasStatus_t cublasMpLoggerSetFile(FILE* file);

cublasStatus_t cublasMpLoggerOpenFile(const char* logFile);

cublasStatus_t cublasMpLoggerSetLevel(int level);

cublasStatus_t cublasMpLoggerSetMask(int mask);

cublasStatus_t cublasMpLoggerForceDisable();

#ifdef __cplusplus
}
#endif
