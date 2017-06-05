#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include "conv.h"
// from beej

void lmcp_packi16 (uint8_t* buf, uint16_t in) {
    *buf++ = in >> 8; *buf++ = in;
}

uint16_t lmcp_unpacki16 (uint8_t* buf) {
    return (buf[0] << 8) | buf[1];
}

uint32_t lmcp_unpacki32(uint8_t *buf)
{
	return (buf[0]<<24) | (buf[1]<<16) | (buf[2]<<8) | buf[3];
}

void lmcp_packi32(uint8_t *buf, uint32_t i)
{
	*buf++ = i>>24; *buf++ = i>>16;
	*buf++ = i>>8;  *buf++ = i;
}

void lmcp_packi64 (uint8_t *buf, uint64_t i) {
    *buf++ = i >> 56;
    *buf++ = i >> 48;
    *buf++ = i >> 40;
    *buf++ = i >> 32;
    *buf++ = i >> 24;
    *buf++ = i >> 16;
    *buf++ = i >> 8;
    *buf++ = i;
}


uint64_t lmcp_unpacki64(uint8_t *buf)
{
	return ((uint64_t)buf[0]<<56) | ((uint64_t)buf[1]<<48) | ((uint64_t)buf[2]<<40) | ((uint64_t)buf[3]<<32) | ((uint64_t)buf[4]<<24) | ((uint64_t)buf[5]<<16) | ((uint64_t)buf[6]<<8) | ((uint64_t)buf[7]);
}


void lmcp_packs16 (uint8_t* buf, int8_t in) {
    lmcp_packi16(buf, *(uint8_t*)&in);
}

void lmcp_packs32 (uint8_t* buf, int32_t in) {
    lmcp_packi32(buf, *(uint8_t*)&in);
}
void lmcp_packs64 (uint8_t* buf, int64_t in) {
    lmcp_packi64(buf, *(uint8_t*)&in);
}

int16_t lmcp_unpacks16 (uint8_t* buf) {
    int16_t out = lmcp_unpacki16(buf);
    return *(int16_t*)&out;
}
int32_t lmcp_unpacks32 (uint8_t* buf) {
    int16_t out = lmcp_unpacki32(buf);
    return *(int32_t*)&out;
}
int64_t lmcp_unpacks64 (uint8_t* buf) {
    int16_t out = lmcp_unpacki32(buf);
    return *(int64_t*)&out;
}
// macros for packing floats and doubles:
#define pack754_32(f) (pack754((f), 32, 8))
#define pack754_64(f) (pack754((f), 64, 11))
#define unpack754_32(i) (unpack754((i), 32, 8))
#define unpack754_64(i) (unpack754((i), 64, 11))


// pack754() -- pack a floating point number into IEEE-754 format
 
 long long pack754(long double f, unsigned bits, unsigned expbits)
{
	long double fnorm;
	int shift;
	long long sign, exp, significand;
	unsigned significandbits = bits - expbits - 1; // -1 for sign bit

	if (f == 0.0) return 0; // get this special case out of the way

	// check sign and begin normalization
	if (f < 0) { sign = 1; fnorm = -f; }
	else { sign = 0; fnorm = f; }

	// get the normalized form of f and track the exponent
	shift = 0;
	while(fnorm >= 2.0) { fnorm /= 2.0; shift++; }
	while(fnorm < 1.0) { fnorm *= 2.0; shift--; }
	fnorm = fnorm - 1.0;

	// calculate the binary form (non-float) of the significand data
	significand = fnorm * ((1LL<<significandbits) + 0.5f);

	// get the biased exponent
	exp = shift + ((1<<(expbits-1)) - 1); // shift + bias

	// return the final answer
	return (sign<<(bits-1)) | (exp<<(bits-expbits-1)) | significand;
}


// unpack754() -- unpack a floating point number from IEEE-754 format
 
long double unpack754(long long i, unsigned bits, unsigned expbits)
{
	long double result;
	long long shift;
	unsigned bias;
	unsigned significandbits = bits - expbits - 1; // -1 for sign bit

	if (i == 0) return 0.0;

	// pull the significand
	result = (i&((1LL<<significandbits)-1)); // mask
	result /= (1LL<<significandbits); // convert back to float
	result += 1.0f; // add the one back on

	// deal with the exponent
	bias = (1<<(expbits-1)) - 1;
	shift = ((i>>significandbits)&((1LL<<expbits)-1)) - bias;
	while(shift > 0) { result *= 2.0; shift--; }
	while(shift < 0) { result /= 2.0; shift++; }

	// sign it
	result *= (i>>(bits-1))&1? -1.0: 1.0;

	return result;
}

void lmcp_pack_float(uint8_t* buf, float in) {
   uint32_t l = pack754_32(in);
   lmcp_packi32(buf, l);
}

float lmcp_unpack_float(uint8_t* buf) {
    uint32_t p = lmcp_unpacki32(buf);
    return (float) unpack754_32(p);
}

void lmcp_pack_double(uint8_t* buf, double in) {
   uint64_t l = pack754_64(in);
   lmcp_packi64(buf, l);
}

double lmcp_unpack_double(uint8_t* buf) {
    uint64_t p = lmcp_unpacki64(buf);
    return (double) unpack754_64(p);
} 

void lmcp_pack_byte(uint8_t* buf, uint8_t in) {
    *buf = in;
}

uint8_t lmcp_unpack_byte(uint8_t* buf) {
    return *buf;
}

char lmcp_unpack_char(uint8_t* buf) {
    return *buf;
}

void lmcp_pack_char(uint8_t* buf, char in) {
    *buf = in;
}

uint16_t string_len(const char* in) {
    uint16_t s = 0;
    while (*in != '\0') {
        s++;
        in++;

    }

    return s;
}


void lmcp_pack_string(uint8_t* buf, char* in) {
    uint16_t len = string_len(in);
    lmcp_packi16(buf, len);
    buf += 2;
    for (uint16_t i = 0; i < len; i++)
        *buf++ = *in++;
}

uint16_t lmcp_unpack_stringlen(uint8_t* buf) {
    uint16_t len = lmcp_unpacki16(buf) + 1;
    return len;
}

void lmcp_unpack_string(uint8_t* buf, char* out, uint16_t len) {
    char* outbuf = out;
    for (uint16_t i = 0; i < len; i++)
        *outbuf++ = *buf++;
}

float float_packupack(float in) {
    uint8_t buf[4];
    lmcp_pack_float(buf, in);
    return lmcp_unpack_float(buf);
}
