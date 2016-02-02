/* Fake library to simulate some features of Libescdf */

typedef struct {
    FILE *fd;
    unsigned int number_of_physical_dimensions;
    unsigned int absolute_or_reduced_coordinates;
    unsigned int dimension_types[3];
    char embedded_system[3];
    unsigned int space_group;
    unsigned int number_of_sites;
    unsigned int number_of_species;
} escdf_geometry_t;

void escdf_f03_geometry_new(escdf_geometry_t *geometry, FILE *fd, const char *path) {
    geometry = (escdf_geometry_t *)malloc(sizeof(escdf_geometry_t));
    fd = open(path, "r");
    geometry->fd = fd;
}

void escdf_f03_geometry_read_metadata(escdf_geometry_t *geometry) {
    char tmp[81], emb[4];
    int dim, dtypes[3];

    fscanf("%s %d\n", tmp, &dim);
    geometry->number_of_physical_dimensions = dim;
    fscanf("%s %d\n", tmp, &dim);
    absolute_or_reduced_coordinates = dim;
    fscanf("%s %d\n", tmp, &dim);
    dimension_types = dim;
    fscanf("%s %d\n", tmp, &dim);
    embedded_system = dim;
    fscanf("%s %d\n", tmp, &dim);
    space_group = dim;
    fscanf("%s %d\n", tmp, &dim);
    number_of_sites = dim;
    fscanf("%s %d\n", tmp, &dim);
    number_of_species = dim;
}
