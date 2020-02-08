# ==============================================================
# File generated on Sat Apr 20 17:49:30 +0300 2019
# Vivado(TM) HLS - High-Level Synthesis from C, C++ and SystemC v2018.3 (64-bit)
# SW Build 2405991 on Thu Dec  6 23:38:27 MST 2018
# IP Build 2404404 on Fri Dec  7 01:43:56 MST 2018
# Copyright 1986-2018 Xilinx, Inc. All Rights Reserved.
# ==============================================================
add_files -tb ../test.c -cflags { -Wno-unknown-pragmas}
add_files yuz_digit/sigmoid.h
add_files yuz_digit/sigmoid.c
add_files yuz_digit/relu.h
add_files yuz_digit/relu.c
add_files yuz_digit/main.c
add_files yuz_digit/linear.h
add_files yuz_digit/linear.c
add_files yuz_digit/layer.h
add_files yuz_digit/layer.c
add_files yuz_digit/flatten.h
add_files yuz_digit/flatten.c
add_files yuz_digit/conv.h
add_files yuz_digit/conv.c
set_part xc7z020clg484-1
create_clock -name default -period 10
