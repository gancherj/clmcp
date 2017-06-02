#include <stdint.h>
#include <stdbool.h>

inline void lmcp_pack_bool(bool b, uint8_t* head) {
    if (b == true)
        *head = (uint8_t)1;
    else
        *head = (uint8_t)0;
    head++;
}

inline void lmcp_pack_byte(uint8_t i, uint8_t* head) {
    *head = i;
    head++;
}

inline void lmcp_pack_char(char c, uint8_t* head) {
    *head = c;
    head++;
}

inline void lmcp_pack_uint16(uint16_t i, uint8_t* head) {
    uint16_t big_end = i16_htonl(i);
    uint8_t* data = (*uint8_t) &big_end;
    head[0] = data[0];
    head[1] = data[1];
    head += 2;
}

inline void lmcp_pack_uint32(uint32_t i, uint8_t* head) {

}

inline void lmcp_pack_string(const char* s, uint8_t* head) {
    // does not include null termination
    uint16_t slen = 0; // TODO manually
    lcmp_pack_uint16(s, head);
    for (uint16_t i = 0; i < slen; i++)
        head[i] = ((const uint8_t*)s)[i];
    head += slen;

}

// todo: pack float, pack signed integer




