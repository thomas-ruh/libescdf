      module escdf_variables
        
        character*3  embedded_system,symmorphic
        double precision,dimension(:,:),allocatable :: site_positions
        double precision,dimension(:,:),allocatable :: lattice_vectors
        double precision,dimension(:,:,:),allocatable :: local_rotations
        character*10, dimension(:),allocatable :: species_names
        character*2, dimension(:),allocatable :: chemical_symbols
        double precision,dimension(:,:),allocatable :: reduced_symmetry_translations
        double precision,dimension(:),allocatable :: atomic_numbers
        integer,dimension(:),allocatable :: species_at_sites
        integer,dimension(:,:,:),allocatable :: reduced_symmetry_matrices
        integer      number_of_species,space_group,number_of_sites
        integer      number_of_symmetry_operations,number_of_physical_dimensions
        integer      absolute_or_reduced_coordinates

      end module escdf_variables
