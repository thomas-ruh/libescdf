/* Fake library to simulate some features of Libescdf */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>

typedef struct escdf_geometry_type {
    char embedded_system[4];
    unsigned int number_of_physical_dimensions;
    unsigned int absolute_or_reduced_coordinates;
    unsigned int dimension_types[3];
    unsigned int space_group;
    unsigned int number_of_sites;
    unsigned int number_of_species;
} escdf_geometry_t;


void escdf_geometry_new(escdf_geometry_t **geometry);
void escdf_geometry_read_metadata(escdf_geometry_t *geometry, const char *path);
void escdf_geometry_write_metadata(escdf_geometry_t *geometry, const char *path);
void escdf_geometry_free(escdf_geometry_t *geometry);


void escdf_geometry_new(escdf_geometry_t **geometry) {

    printf("NEW: creating data structure\n"); fflush(stdout);
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
}

void escdf_geometry_read_metadata(escdf_geometry_t *geometry, const char *path) {
    char *key, *val;
    FILE *fd;

    assert(geometry != NULL);

    fd = fopen(path, "r");
    assert(fd != NULL);

    key = (char *)malloc(128*sizeof(char));
    assert(key != NULL);
    key[0] = '\0';
    val = (char *)malloc(128*sizeof(char));
    assert(val != NULL);
    val[0] = '\0';

    printf("READ: reading metadata\n"); fflush(stdout);
    fscanf(fd, "%s", key);
    fscanf(fd, "%s", val);
    geometry->number_of_physical_dimensions = atoi(val);
    printf("    * %s OK\n", key); fflush(stdout);
    fscanf(fd, "%s", key);
    fscanf(fd, "%s", val);
    geometry->absolute_or_reduced_coordinates = atoi(val);
    printf("    * %s OK\n", key); fflush(stdout);
    fscanf(fd, "%s", key);
    fscanf(fd, "%s", val);
    geometry->dimension_types[0] = atoi(val);
    fscanf(fd, "%s", val);
    geometry->dimension_types[1] = atoi(val);
    fscanf(fd, "%s", val);
    geometry->dimension_types[2] = atoi(val);
    printf("    * %s OK\n", key); fflush(stdout);
    fscanf(fd, "%s", key);
    fscanf(fd, "%s", val);
    strncpy(geometry->embedded_system, val, 3);
    printf("    * %s OK\n", key); fflush(stdout);
    fscanf(fd, "%s", key);
    fscanf(fd, "%s", val);
    geometry->space_group = atoi(val);
    printf("    * %s OK\n", key); fflush(stdout);
    fscanf(fd, "%s", key);
    fscanf(fd, "%s", val);
    geometry->number_of_sites = atoi(val);
    printf("    * %s OK\n", key); fflush(stdout);
    fscanf(fd, "%s", key);
    fscanf(fd, "%s", val);
    geometry->number_of_species = atoi(val);
    printf("    * %s OK\n", key); fflush(stdout);
}

void escdf_geometry_write_metadata(escdf_geometry_t *geometry, const char *path) {
    char key[128];
    int dim, dtypes[3];
    FILE *fd;

    assert(geometry != NULL);

    printf("WRITE: opening '%s' for writing\n", path); fflush(stdout);
    fd = fopen(path, "w");
    assert(fd != NULL);

    strcpy(key, "number_of_physical_dimensions");
    fprintf(fd, "%s %d\n", key, geometry->number_of_physical_dimensions);
    printf("    * %s OK\n", key); fflush(stdout);
    strcpy(key, "absolute_or_reduced_coordinates");
    fprintf(fd, "%s %d\n", key, geometry->absolute_or_reduced_coordinates);
    printf("    * %s OK\n", key); fflush(stdout);
    strcpy(key, "dimension_types");
    fprintf(fd, "%s %d %d %d\n", key, geometry->dimension_types[0], geometry->dimension_types[1], geometry->dimension_types[2]);
    printf("    * %s OK\n", key); fflush(stdout);
    strcpy(key, "embedded_system");
    fprintf(fd, "%s %s\n", key, geometry->embedded_system);
    printf("    * %s OK\n", key); fflush(stdout);
    strcpy(key, "space_group");
    fprintf(fd, "%s %d\n", key, geometry->space_group);
    printf("    * %s OK\n", key); fflush(stdout);
    strcpy(key, "number_of_sites");
    fprintf(fd, "%s %d\n", key, geometry->number_of_sites);
    printf("    * %s OK\n", key); fflush(stdout);
    strcpy(key, "number_of_species");
    fprintf(fd, "%s %d\n", key, geometry->number_of_species);
    printf("    * %s OK\n", key); fflush(stdout);
}

void escdf_geometry_free(escdf_geometry_t *geometry) {
    assert(geometry != NULL);
    free(geometry);
}
