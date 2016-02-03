/* Fake library to simulate some features of Libescdf */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>

typedef struct escdf_geometry_type {
    FILE *fd;
    char embedded_system[4];
    unsigned int number_of_physical_dimensions;
    unsigned int absolute_or_reduced_coordinates;
    unsigned int dimension_types[3];
    unsigned int space_group;
    unsigned int number_of_sites;
    unsigned int number_of_species;
} escdf_geometry_t;


void escdf_geometry_new(escdf_geometry_t **geometry, const char *path, const char *mode);
void escdf_geometry_read_metadata(escdf_geometry_t *geometry);
void escdf_geometry_write_metadata(escdf_geometry_t *geometry);
void escdf_geometry_free(escdf_geometry_t *geometry);
void escdf_geometry_set_file(escdf_geometry_t *geometry, const char *path, const char *mode);


void escdf_geometry_new(escdf_geometry_t **geometry, const char *path, const char *mode) {

    printf("NEW: creating data structure for %s\n", path); fflush(stdout);
    *geometry = (escdf_geometry_t *)malloc(sizeof(escdf_geometry_t));
    assert(*geometry != NULL);

    memset((*geometry)->embedded_system, 0, 1);
    (*geometry)->number_of_physical_dimensions = 0;
    (*geometry)->absolute_or_reduced_coordinates = 0;
    (*geometry)->dimension_types[0] = 0;
    (*geometry)->dimension_types[1] = 0;
    (*geometry)->dimension_types[2] = 0;
    (*geometry)->space_group = 0;
    (*geometry)->number_of_sites = 0;
    (*geometry)->number_of_species = 0;

    (*geometry)->fd = fopen(path, mode);
    assert((*geometry)->fd != NULL);
}

void escdf_geometry_read_metadata(escdf_geometry_t *geometry) {
    char *key, *val;

    assert(geometry != NULL);

    key = (char *)malloc(128*sizeof(char));
    assert(key != NULL);
    key[0] = '\0';
    val = (char *)malloc(128*sizeof(char));
    assert(val != NULL);
    val[0] = '\0';

    printf("READ: reading metadata\n"); fflush(stdout);
    fscanf(geometry->fd, "%s", key);
    fscanf(geometry->fd, "%s", val);
    geometry->number_of_physical_dimensions = atoi(val);
    printf("    * %s OK\n", key); fflush(stdout);
    fscanf(geometry->fd, "%s", key);
    fscanf(geometry->fd, "%s", val);
    geometry->absolute_or_reduced_coordinates = atoi(val);
    printf("    * %s OK\n", key); fflush(stdout);
    fscanf(geometry->fd, "%s", key);
    fscanf(geometry->fd, "%s", val);
    geometry->dimension_types[0] = atoi(val);
    fscanf(geometry->fd, "%s", val);
    geometry->dimension_types[1] = atoi(val);
    fscanf(geometry->fd, "%s", val);
    geometry->dimension_types[2] = atoi(val);
    printf("    * %s OK\n", key); fflush(stdout);
    fscanf(geometry->fd, "%s", key);
    fscanf(geometry->fd, "%s", val);
    strncpy(geometry->embedded_system, val, 3);
    printf("    * %s OK\n", key); fflush(stdout);
    fscanf(geometry->fd, "%s", key);
    fscanf(geometry->fd, "%s", val);
    geometry->space_group = atoi(val);
    printf("    * %s OK\n", key); fflush(stdout);
    fscanf(geometry->fd, "%s", key);
    fscanf(geometry->fd, "%s", val);
    geometry->number_of_sites = atoi(val);
    printf("    * %s OK\n", key); fflush(stdout);
    fscanf(geometry->fd, "%s", key);
    fscanf(geometry->fd, "%s", val);
    geometry->number_of_species = atoi(val);
    printf("    * %s OK\n", key); fflush(stdout);
}

void escdf_geometry_write_metadata(escdf_geometry_t *geometry) {
    char key[128];
    int dim, dtypes[3];

    assert(geometry != NULL);

    printf("WRITE: rewinding file for writing\n"); fflush(stdout);
    rewind(geometry->fd);   

    strcpy(key, "number_of_physical_dimensions");
    fprintf(geometry->fd, "%s %d\n", key, geometry->number_of_physical_dimensions);
    printf("    * %s OK\n", key); fflush(stdout);
    strcpy(key, "absolute_or_reduced_coordinates");
    fprintf(geometry->fd, "%s %d\n", key, geometry->absolute_or_reduced_coordinates);
    printf("    * %s OK\n", key); fflush(stdout);
    strcpy(key, "dimension_types");
    fprintf(geometry->fd, "%s %d %d %d\n", key, geometry->dimension_types[0], geometry->dimension_types[1], geometry->dimension_types[2]);
    printf("    * %s OK\n", key); fflush(stdout);
    strcpy(key, "embedded_system");
    fprintf(geometry->fd, "%s %s\n", key, geometry->embedded_system);
    printf("    * %s OK\n", key); fflush(stdout);
    strcpy(key, "space_group");
    fprintf(geometry->fd, "%s %d\n", key, geometry->space_group);
    printf("    * %s OK\n", key); fflush(stdout);
    strcpy(key, "number_of_sites");
    fprintf(geometry->fd, "%s %d\n", key, geometry->number_of_sites);
    printf("    * %s OK\n", key); fflush(stdout);
    strcpy(key, "number_of_species");
    fprintf(geometry->fd, "%s %d\n", key, geometry->number_of_species);
    printf("    * %s OK\n", key); fflush(stdout);
}

void escdf_geometry_free(escdf_geometry_t *geometry) {

    printf("FREE: cleaning the mess\n");
    assert(geometry != NULL);
    if ( geometry->fd != NULL ) {
        fclose(geometry->fd);
    }
    free(geometry);
}

void escdf_geometry_set_file(escdf_geometry_t *geometry, const char *path, const char *mode) {

    printf("SET_FILE: switching to '%s' with mode '%s'\n", path, mode);
    if ( geometry->fd != NULL ) {
        fclose(geometry->fd);
    }
    geometry-> fd = fopen(path, mode);
    assert(geometry->fd != NULL);
}
