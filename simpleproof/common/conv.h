#pragma once
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include "conv.h"
// from beej

size_t lmcp_pack_uint16_t (uint8_t* buf, uint16_t in) ;

void lmcp_unpack_uint16_t (uint8_t** buf, size_t *size_remain, uint16_t *out) ;

void lmcp_unpack_uint32_t(uint8_t **buf, size_t * size_remain, uint32_t *out);
size_t lmcp_pack_uint32_t(uint8_t *buf, uint32_t i);

size_t lmcp_pack_uint64_t (uint8_t *buf, uint64_t i) ;


void lmcp_unpack_uint64_t(uint8_t **buf, size_t * size_remain, uint64_t *out);


size_t lmcp_pack_int16_t (uint8_t* buf, int8_t in) ;

size_t lmcp_pack_int32_t (uint8_t* buf, int32_t in) ;
size_t lmcp_pack_int64_t (uint8_t* buf, int64_t in) ;

void lmcp_unpack_int16_t (uint8_t** buf, size_t * size_remain, int16_t* out) ;
void lmcp_unpack_int32_t (uint8_t** buf, size_t * size_remain, int32_t* out) ;
void lmcp_unpack_int64_t (uint8_t** buf, size_t * size_remain, int64_t* out) ;

void lmcp_unpack_8byte (uint8_t** buf, size_t * size_remain, char* out);
void lmcp_unpack_4byte (uint8_t** buf, size_t * size_remain, char* out);
//
/*
size_t lmcp_pack_float(uint8_t* buf, float in) ;

void lmcp_unpack_float(uint8_t** buf, size_t * size_remain, float* out) ;

size_t lmcp_pack_double(uint8_t* buf, double in) ;

void lmcp_unpack_double(uint8_t** buf, size_t * size_remain, double* out) ;
*/
size_t lmcp_pack_uint8_t(uint8_t* buf, uint8_t in) ;

void lmcp_unpack_uint8_t(uint8_t** buf, size_t * size_remain, uint8_t* out) ;

void lmcp_unpack_char(uint8_t** buf, size_t * size_remain, char* out) ;

size_t lmcp_pack_char(uint8_t* buf, char in) ;
/*
uint16_t string_len(const char* in) ;


size_t lmcp_pack_string(uint8_t* buf, char* in) ;

uint16_t lmcp_unpack_stringlen(uint8_t* buf) ;
void lmcp_unpack_string(uint8_t* buf, char* out, uint16_t len) ;
*/


int lmcp_unpack_structheader(uint8_t** inb, size_t* size_remain, char* seriesname, uint32_t* objtype, uint16_t* objseries);
