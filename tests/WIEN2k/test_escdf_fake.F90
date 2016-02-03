program testf_escdf_fake

    use iso_c_binding
    use fescdf_geometry

    implicit none

    character(kind=c_char, len=*), parameter :: test_inp = C_CHAR_"test-read.tmp"//C_NULL_CHAR
    character(kind=c_char, len=*), parameter :: test_out = C_CHAR_"test-write.tmp"//C_NULL_CHAR

    type(fescdf_geometry_t) :: geometry

    call fescdf_geometry_new(geometry)
    call fescdf_geometry_read_metadata(geometry, test_inp)
    call fescdf_geometry_write_metadata(geometry, test_out)
    call fescdf_geometry_free(geometry)

end program testf_escdf_fake
