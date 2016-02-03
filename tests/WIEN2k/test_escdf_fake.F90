program testf_escdf_fake

    use iso_c_binding
    use fescdf_geometry

    implicit none

    character(kind=c_char, len=*), parameter :: test_read = C_CHAR_"test-read.tmp"//C_NULL_CHAR
    character(kind=c_char, len=*), parameter :: test_write = C_CHAR_"test-write.tmp"//C_NULL_CHAR
    character(kind=c_char, len=*), parameter :: test_rmode = C_CHAR_"r"//C_NULL_CHAR
    character(kind=c_char, len=*), parameter :: test_wmode = C_CHAR_"w+"//C_NULL_CHAR

    type(fescdf_geometry_t) :: geometry

    call fescdf_geometry_new(geometry, test_read, test_rmode)
    call fescdf_geometry_read_metadata(geometry)
    call fescdf_geometry_set_file(geometry, test_write, test_wmode)
    call fescdf_geometry_write_metadata(geometry)
    call fescdf_geometry_free(geometry)

end program testf_escdf_fake
