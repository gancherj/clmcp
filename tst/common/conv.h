#pragma once
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include "conv.h"
// from beej

void lmcp_pack_uint16_t (uint8_t* buf, uint16_t in) ;

size_t lmcp_unpack_uint16_t (uint8_t* buf, uint16_t *out) ;

size_t lmcp_unpack_uint32_t(uint8_t *buf, uint32_t *out);
void lmcp_pack_uint32_t(uint8_t *buf, uint32_t i);

void lmcp_pack_uint64_t (uint8_t *buf, uint64_t i) ;


size_t lmcp_unpack_uint64_t(uint8_t *buf, uint64_t *out);


void lmcp_pack_int16_t (uint8_t* buf, int8_t in) ;

void lmcp_pack_int32_t (uint8_t* buf, int32_t in) ;
void lmcp_pack_int64_t (uint8_t* buf, int64_t in) ;

size_t lmcp_unpack_int16_t (uint8_t* buf, int16_t* out) ;
size_t lmcp_unpack_int32_t (uint8_t* buf, int32_t* out) ;
size_t lmcp_unpack_int64_t (uint8_t* buf, int64_t* out) ;
//
/*
void lmcp_pack_float(uint8_t* buf, float in) ;

size_t lmcp_unpack_float(uint8_t* buf, float* out) ;

void lmcp_pack_double(uint8_t* buf, double in) ;

size_t lmcp_unpack_double(uint8_t* buf, double* out) ;
*/
void lmcp_pack_uint8_t(uint8_t* buf, uint8_t in) ;

size_t lmcp_unpack_uint8_t(uint8_t* buf, uint8_t* out) ;

size_t lmcp_unpack_char(uint8_t* buf, char* out) ;

void lmcp_pack_char(uint8_t* buf, char in) ;

uint16_t string_len(const char* in) ;


void lmcp_pack_string(uint8_t* buf, char* in) ;

uint16_t lmcp_unpack_stringlen(uint8_t* buf) ;
void lmcp_unpack_string(uint8_t* buf, char* out, uint16_t len) ;

