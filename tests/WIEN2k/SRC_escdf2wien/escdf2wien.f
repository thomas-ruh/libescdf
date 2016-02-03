      program escdf2wien

      use escdf_variables 
      use fescdf_geometry
      use iso_c_binding

      implicit none

      integer      number_of_commandline_arguments,error_handling
      integer      multiplicity
      character*80 parseline,inputfile_name,outputfile_name,case_name
      character*80 name_of_structure
      character*10 space_group_symbol
      character*4  mode_of_calculation,lattice_type,relativity_method, units
!     relativity_method has to be put in section settings (own parser?)
      double precision translation_checksum
      double precision,dimension(3) :: lattice_parameters, lattice_angles
      double precision,dimension(:),allocatable ::  first_gridpoints,last_gridpoints
!     gridpoints (number, first, last) has to be put in section basis-set (own parser?)
      integer,dimension(:),allocatable :: number_of_gridpoints, dimension_types
      integer      i,j,k,site_counter,species_counter,symm_op_counter
      integer      symm_number_check,first_site_of_species
      character(kind=c_char, len=*), parameter :: test_read = &
                                                  C_CHAR_"test-read"//C_NULL_CHAR
      character(kind=c_char, len=*), parameter :: test_rmode = &
                                                  C_CHAR_"r"//C_NULL_CHAR
      type(fescdf_geometry_t) :: geometry
                                               
!     Initialization

!      name_of_structure=''
!      lattice_parameters(:)=0.d0   !ONLY FOR TESTING
!      lattice_angles(:)=0.d0       !ONLY FOR TESTING
!      units='bohr'                 !ONLY FOR TESTING
!      relativity_method='RELA'     !ONLY FOR TESTING
!      lattice_type='B'             !ONLY FOR TESTING
!      space_group_symbol='I-4'     !ONLY FOR TESTING
!      site_positions(:,:)=0.d0      !ONLY FOR TESTING
!      site_counter=1               !ONLY FOR TESTING

!      number_of_commandline_arguments=iargc()
!      if (number_of_commandline_arguments.ne.1) then
!          stop 'Error: Exactly ONE commandline argument (case.escdf) must be &
!                given!'
!      endif

!      call getarg(1,inputfile_name)
!      open(25,file=inputfile_name,status='old',iostat=error_handling)
!      if (error_handling.ne.0) stop 'Error: Input-File could not be opened.'

!      do i=1,80
!!         if(inputfile_name(i:i+6).eq.'.escdf') then
!         if(inputfile_name(i:i+4).eq.'.txt') then
!            case_name=inputfile_name(1:i-1)
!            exit
!         endif
!         if(i.eq.80) then
!            stop 'Error: No properly named escdf-file specified!'
!         endif
!      enddo
!      outputfile_name=trim(case_name)//'.struct'

!########################### reading ESCDF-file ###########################

       call fescdf_geometry_new(geometry, test_read, test_rmode)

       call fescdf_geometry_read_metadata(geometry)

!       call fescdf_geometry_get_number_of_physical_dimensions(

!       call fescdf_geometry_get_absolute_or_reduced_coordinates(

!       call fescdf_geometry_get_dimension_types(

!       call fescdf_geometry_get_embedded_system(

!       call fescdf_geometry_get_space_group(

!       call fescdf_geometry_get_number_of_sites(

!       call fescdf_geometry_get_number_of_species(

!###########################   end of reading   ###########################

! test with yann

       open(99,file='metadata.txt',status='unknown')
       write(99,*) 'number_of_physical_dimensions', number_of_physical_dimensions
       write(99,*) 'absolute_or_reduced_coordinates', absolute_or_reduced_coordinates
       write(99,*) 'dimension_types', dimension_types
       write(99,*) 'embedded_system', embedded_system
       write(99,*) 'space_group', space_group
       write(99,*) 'number_of_sites', number_of_sites
       write(99,*) 'number_of_species', number_of_species

!      open(20,file=outputfile_name,status='new',iostat=error_handling)
!      if (error_handling.ne.0) stop 'Error: Output-File already present!'

!      if(name_of_structure.ne.'') then
!        write(20,'(a80)') name_of_structure
!      else
!        write(20,'(a80)') case_name
!      endif
!
!      write(20,'(a4,"LATTICE,NONEQUIV.ATOMS ",i3,2x,i3,x,a10)') lattice_type,&
!                     number_of_species,space_group,space_group_symbol
!      write(20,'("MODE OF CALC=",a4,x,"unit=",a4)') relativity_method, units
!      write(20,'(6f10.6)') (lattice_parameters(k),k=1,3),(lattice_angles(k),k=1,3)
!!! LOOP OVER ATOMS (REPLACE 1 WITH i bzw. CORRECT site_counter)!
!      
!      close(20)
!      close(25)

      stop 'escdf2wien finished'
      end
