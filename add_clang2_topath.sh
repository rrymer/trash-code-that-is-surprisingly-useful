CLANG_INCLUDE=~/code/llvm/include
CLANG_BIN=~/code/llvm/build/Debug+Asserts/bin
CLANG_LIB=~/code/llvm/build/Debug+Asserts/lib
OPENMP_INCLUDE=~/code/libomp_oss/exports/common/include
OPENMP_LIB=~/code/libomp_oss/exports/mac_32e/lib.thin

echo "OpenMP Runtime Include Path : " ${OPENMP_INCLUDE}
echo "OpenMP Runtime Lib Path     : " ${OPENMP_LIB}

(echo 'export PATH='${CLANG_BIN}':$PATH';
    echo 'export C_INCLUDE_PATH='${CLANG_INCLUDE}':'${OPENMP_INCLUDE}':$C_INCLUDE_PATH'; 
    echo 'export CPLUS_INCLUDE_PATH='${CLANG_INCLUDE}':'${OPENMP_INCLUDE}':$CPLUS_INCLUDE_PATH';
    echo 'export LIBRARY_PATH='${CLANG_LIB}':'${OPENMP_LIB}':$LIBRARY_PATH';
    echo 'export DYLD_LIBRARY_PATH='${CLANG_LIB}':'${OPENMP_LIB}':$DYLD_LIBRARY_PATH}') >> ~/.zlogin

echo "LLVM+Clang+OpenMP is now accessible through [ clang2 ] via terminal and does not conflict with Apple's clang"