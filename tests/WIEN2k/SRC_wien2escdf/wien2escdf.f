!!!   TODO:
!!!
!!!   * lattice_vectors
!!!   * local_rotations for all sites (read from case.output0???)
!!!
      program wien2escdf

      use escdf_variables 
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

!######################### 'Fixed' settings of WIEN2k #########################
      number_of_physical_dimensions=3
      absolute_or_reduced_coordinates=2 ! 2=reduced coordinates
      allocate(dimension_types(number_of_physical_dimensions))
      allocate(lattice_vectors(number_of_physical_dimensions,&
                               number_of_physical_dimensions))
      dimension_types(:)=1
      embedded_system='no' !check with pblaha, if wien can do embedded
!##############################################################################

      number_of_commandline_arguments=iargc()
      if (number_of_commandline_arguments.ne.1) then
          stop 'Error: Exactly ONE commandline argument (case.struct) must be &
                given!'
      endif

      call getarg(1,inputfile_name)
      open(20,file=inputfile_name,status='old',iostat=error_handling)
      if (error_handling.ne.0) stop 'Error: Input-File could not be opened.'

      do i=1,80
         if(inputfile_name(i:i+7).eq.'.struct') then
            case_name=inputfile_name(1:i-1)
            exit
         endif
         if(i.eq.80) then
            stop 'Error: No properly named struct-file specified!'
         endif
      enddo
!      outputfile_name=trim(case_name)//'.escdf'
      outputfile_name=trim(case_name)//'.txt'

!######################### Parsing WIEN2k struct-file #########################      
      
      read(20,'(a80)') name_of_structure

      read(20,'(a4,23x,i3,1x,i4,1x,a10,/,13x,a4,6x,a4)') lattice_type, &
                number_of_species, space_group, space_group_symbol, &
                relativity_method, units

      read(20,'(6F10.6)') (lattice_parameters(k),k=1,3), (lattice_angles(k),k=1,3)
      

      
      i=0
      number_of_sites=0
      do 
        read(20,'(a80)') parseline
        if(parseline(11:14).eq.'MULT') then
           read(parseline(16:17),'(i2)') multiplicity
           number_of_sites=number_of_sites+multiplicity
           i=i+1
           if(i.eq.number_of_species) exit
        endif
        if(parseline(11:14).eq.'NUMB') then
           stop 'Error: Not all multiplicities read!'
        endif
      enddo

      rewind(20)
      
      allocate(species_at_sites(number_of_sites))
      allocate(species_names(number_of_species))
      allocate(chemical_symbols(number_of_species))
      allocate(atomic_numbers(number_of_species))
      allocate(number_of_gridpoints(number_of_species))
      allocate(first_gridpoints(number_of_species))
      allocate(last_gridpoints(number_of_species))
      allocate(site_positions(number_of_physical_dimensions,number_of_sites))
      allocate(local_rotations(number_of_physical_dimensions,&
                               number_of_physical_dimensions,&
                               number_of_sites))
      
      read(20,'(///)')
      site_counter=0
      species_counter=0
      local_rotations(:,:,:)=0.d0
      do
         read(20,'(a80)') parseline
         if(parseline(11:16).eq.'NUMBER') then
           read(parseline(3:4),'(i2)') number_of_symmetry_operations
           exit
         elseif(parseline(1:4).eq.'ATOM') then
           site_counter=site_counter+1
           species_counter=species_counter+1
           read(parseline(13:48),'(f10.8,3x,f10.8,3x,f10.8)') &
                                  ( site_positions(k,site_counter), k=1,3)
           species_at_sites(site_counter)=species_counter
           read(20,'(15x,i2)') multiplicity
           if(multiplicity.ne.1) then
              do j=1,multiplicity-1
                 read(20,'(a80)') parseline
                 site_counter=site_counter+1
                 read(parseline(13:48),'(f10.8,3x,f10.8,3x,f10.8)') &
                                        ( site_positions(k,site_counter), k=1,3)
                 species_at_sites(site_counter)=species_counter
              enddo
           endif
           read(20,'(a80)') parseline
           read(parseline(1:65),'(a10,5x,i5,5x,f10.9,5x,f10.5,5x,f10.5)') &
                                  species_names(species_counter),&
                                  number_of_gridpoints(species_counter), &
                                  first_gridpoints(species_counter),&
                                  last_gridpoints(species_counter),&
                                  atomic_numbers(species_counter)
           read(parseline(1:2),'(a2)') chemical_symbols(species_counter)
         endif
         first_site_of_species=site_counter-multiplicity+1
         read(20,'(20x,3f10.8)') ( local_rotations(1,k,first_site_of_species), k=1,3)
         read(20,'(20x,3f10.8)') ( local_rotations(2,k,first_site_of_species), k=1,3)
         read(20,'(20x,3f10.8)') ( local_rotations(3,k,first_site_of_species), k=1,3)
      enddo

      allocate(reduced_symmetry_matrices(number_of_physical_dimensions,&
                                         number_of_physical_dimensions,&
                                         number_of_symmetry_operations))
      allocate(reduced_symmetry_translations(number_of_physical_dimensions,&
                                             number_of_symmetry_operations))
      translation_checksum=0.d0
      symm_op_counter=0
!
! reduced_symmetry_matrices stored columnwise for each symmetry operation
!
      do
        symm_op_counter=symm_op_counter+1
        read(20,'(3i2,f11.8)') (reduced_symmetry_matrices(1,k,symm_op_counter),k=1,3),&
                               reduced_symmetry_translations(1,symm_op_counter)
        read(20,'(3i2,f11.8)') (reduced_symmetry_matrices(2,k,symm_op_counter),k=1,3),&
                               reduced_symmetry_translations(2,symm_op_counter)
        read(20,'(3i2,f11.8)') (reduced_symmetry_matrices(3,k,symm_op_counter),k=1,3),&
                               reduced_symmetry_translations(3,symm_op_counter)
        translation_checksum=translation_checksum&
                             +abs(reduced_symmetry_translations(1,symm_op_counter))&
                             +abs(reduced_symmetry_translations(2,symm_op_counter))&
                             +abs(reduced_symmetry_translations(3,symm_op_counter))
        read(20,'(6x,i2)') symm_number_check
        if(symm_number_check.eq.number_of_symmetry_operations) exit
      enddo
       if(translation_checksum.eq.0.d0) then
          symmorphic='yes'
       else
          symmorphic='no'
       endif
       close(20)

!######################### Writing Data in ESCDF-File #########################     

!      open(25,file=outputfile_name,status='new',iostat=error_handling) ! testing
!      if (error_handling.ne.0) stop 'Error: Output-File already present!' ! testing

      

! REFERENCE OUTPUT
!      write(25,*) 'number_of_physical_dimensions', number_of_physical_dimensions
!      write(25,*) number_of_physical_dimensions
!      write(25,*) 'absolute_or_reduced_coordinates', absolute_or_reduced_coordinates
!      write(25,*) absolute_or_reduced_coordinates
!      write(25,*) 'dimension_types', dimension_types
!      write(25,*) dimension_types
!      write(25,*) 'embedded_system', embedded_system
!      write(25,*) embedded_system
!      write(25,*) 'space_group', space_group
!      write(25,*) space_group
!      write(25,*) 'number_of_sites', number_of_sites
!      write(25,*) 'number_of_species', number_of_species
!      write(25,*) number_of_species
!      write(25,*) 'lattice_parameters', lattice_parameters
!      write(25,*) lattice_parameters
!      write(25,*) 'lattice_angles', lattice_angles
!      write(25,*) lattice_angles
!      write(25,*) 'species_names', species_names
!      write(25,*) species_names
!      write(25,*) 'chemical_symbols', chemical_symbols
!      write(25,*) chemical_symbols
!      write(25,*) 'atomic_numbers', atomic_numbers
!      write(25,*) atomic_numbers
!      write(25,*) 'site_positions', site_positions
!      write(25,*) site_positions
!      write(25,*) 'species_at_sites', species_at_sites
!      write(25,*) species_at_sites
!      write(25,*) 'first_gridpoints', first_gridpoints
!      write(25,*) first_gridpoints
!      write(25,*) 'last_gridpoints', last_gridpoints
!      write(25,*) last_gridpoints
!      write(25,*) 'number_of_gridpoints', number_of_gridpoints
!      write(25,*) number_of_gridpoints
!      write(25,*) 'number_of_symmetry_operations', number_of_symmetry_operations
!      write(25,*) 'reduced_symmetry_matrices', reduced_symmetry_matrices
!      write(25,*) reduced_symmetry_matrices
!      write(25,*) 'reduced_symmetry_translations', reduced_symmetry_translations
!      write(25,*) reduced_symmetry_translations
!      write(25,*) 'symmorphic', symmorphic
!      write(25,*) symmorphic
!      write(25,*) 'local_rotations', local_rotations
!      write(25,*) local_rotations
      
!      close(25)

      stop 'wien2escdf finished'
      end
