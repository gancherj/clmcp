#pragma once
#include <stdint.h>

typedef struct {
    uint32_t type;
    // series name, version can also go here
} lmcp_object;

typedef enum {
    ARR_VAR,
    ARR_VARLARGE,
    ARR_FIXED
} array_type;

typedef struct {
    size_t length;
    array_type type;
} array_info;
