;; Author: Joscha Egloff
;; Version: 6402x8_1.0

;; [device(6402)]

;*

    A Source File written for the 6402 Emulator!

*;

hostcall $44 ;* __host_get_cycles(); Will load the number of cycles into the X register! *;

stx *$80$F3 ;* store_x(0x80F3); *;


