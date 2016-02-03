module fescdf_geometry

    use iso_c_binding

    implicit none

    public :: &
        fescdf_geometry_t, &
        fescdf_geometry_new, &
        fescdf_geometry_read_metadata, &
        fescdf_geometry_write_metadata, &
        fescdf_geometry_free

    type :: fescdf_geometry_t
        private
        type(c_ptr) :: ptr = C_NULL_PTR
    end type fescdf_geometry_t

    interface
        subroutine escdf_geometry_new(geometry, path, mode) bind(c)
            import
            type(c_ptr) :: geometry
            character(kind=c_char) :: path(*)
            character(kind=c_char) :: mode(*)
        end subroutine escdf_geometry_new
    end interface
    interface
        subroutine escdf_geometry_read_metadata(geometry) bind(c)
            import
            type(c_ptr), value :: geometry
        end subroutine escdf_geometry_read_metadata
    end interface
    interface
        subroutine escdf_geometry_write_metadata(geometry) bind(c)
            import
            type(c_ptr), value :: geometry
        end subroutine escdf_geometry_write_metadata
    end interface
    interface
        subroutine escdf_geometry_free(geometry) bind(c)
            import
            type(c_ptr), value :: geometry
        end subroutine escdf_geometry_free
    end interface
    interface
        subroutine escdf_geometry_set_file(geometry, path, mode) bind(c)
            import
            type(c_ptr), value :: geometry
            character(kind=c_char) :: path(*)
            character(kind=c_char) :: mode(*)
        end subroutine escdf_geometry_set_file
    end interface

contains

    subroutine fescdf_geometry_new(geometry, path, mode)
        type(fescdf_geometry_t), intent(inout) :: geometry
        character(kind=c_char, len=*), intent(in) :: path
        character(kind=c_char, len=*), intent(in) :: mode

        call escdf_geometry_new(geometry%ptr, path, mode)

    end subroutine fescdf_geometry_new

    subroutine fescdf_geometry_read_metadata(geometry)
        type(fescdf_geometry_t), intent(inout) :: geometry

        call escdf_geometry_read_metadata(geometry%ptr)

    end subroutine fescdf_geometry_read_metadata

    subroutine fescdf_geometry_write_metadata(geometry)
        type(fescdf_geometry_t), intent(in) :: geometry

        call escdf_geometry_write_metadata(geometry%ptr)

    end subroutine fescdf_geometry_write_metadata

    subroutine fescdf_geometry_free(geometry)
        type(fescdf_geometry_t), intent(inout) :: geometry

        call escdf_geometry_free(geometry%ptr)
        geometry%ptr = C_NULL_PTR

    end subroutine fescdf_geometry_free

    subroutine fescdf_geometry_set_file(geometry, path, mode)
        type(fescdf_geometry_t), intent(inout) :: geometry
        character(kind=c_char, len=*), intent(in) :: path
        character(kind=c_char, len=*), intent(in) :: mode

        call escdf_geometry_set_file(geometry%ptr, path, mode)

    end subroutine fescdf_geometry_set_file

end module fescdf_geometry
