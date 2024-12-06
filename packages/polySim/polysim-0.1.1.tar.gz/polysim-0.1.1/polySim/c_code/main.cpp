#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <numpy/arrayobject.h>  // Include if you're using NumPy arrays
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#define MAXNUCLII 2500      // maximum nuclii to be generated
#define MAX_UINT16 65535    // maximum value of unsigned 16 bit integer

#include "main.h"

// Globals
int LL;
int W;
int S;
int HEIGHT;
int NUCLEATION_RATE;
float GROWTH_RATE;
FILE *fpDebug, *fpAvrami;

int scanLine(uint16_t img[], int x1, int x2, int y_up, int y_down, int gray, int np)
{
    int i;
    if (x1 > LL)
        return np;
    if (x2 < 0)
        return np;
    if (x1 < 0)
        x1 = 0;
    if (x2 > LL)
        x2 = LL;
    if (y_up >=0 && y_up <= W) {
        for (i=x1;i<=x2;i++) {
            if (img[i*(W+1)+y_up] == 0) {
                img[i*(W+1)+y_up] = gray;
                np++;
             }
        }
    }
    if (y_down >=0 && y_down <= W) {
        for (i=x1;i<=x2;i++) {
            if (img[i*(W+1)+y_down] == 0) {
                img[i*(W+1)+y_down] = gray;
                np++;
            }
        }
    }
    return np;
}

/** Draws a disk on a 2D array (img)
  * r: radisu, x0,y0: centre  gray: gray value  np: number of non-zero pixels in img
  * Returns np
*/
int drawDisk(uint16_t img[], int r, int x0, int y0, int gray, int np)
{
    int xk, yk, xkp1, ykp1, pk;

    if (gray > 1000) {
        fprintf(fpDebug, "gray = %d\n", gray);
    }

    xk = 0;
    yk = r;

    pk = 1 - r;

    while (xk <= yk) {
        xkp1 = xk + 1;
        if (pk < 0) {
            np = scanLine(img, x0-yk, x0+yk, y0+xk, y0-xk, gray, np);
            ykp1 = yk;
        } else {
            ykp1 = yk - 1;
            np = scanLine(img, x0-xk, x0+xk, y0+yk, y0-yk, gray, np);
            np = scanLine(img, x0-yk, x0+yk, y0+xk, y0-xk, gray, np);
        }
        pk += 2*(xk+1) + (ykp1*ykp1-yk*yk) - (ykp1-yk) + 1;
        xk = xkp1;
        yk = ykp1;
    }
    return np;
}

/** increments diameter of each nuclius
  * d: diameter array  nNuclii: number of nuclii  growthRate: increment in diamter
*/
void incrementDia(float d[], int nNuclii, float growthRate) {
    int i;
    for (i=0;i<nNuclii;i++) {
        d[i] += growthRate;
    }
}

/** generates section profile  diameters of those nuclii/grains which are intersected by z-section
  * d: diameter array  dc: profile diameters  z: z coordinate, zc array: on return will have 1 or -1 values
  * zpos = position of section  nNuclii: number of nuclii/grains
*/
void rsection(float d[], float dc[], int z[], int zc[], int zpos, int nNuclii) {
    int i;
    for (i=0;i<nNuclii;i++) {
        if (d[i] - 2*abs(z[i]-zpos) > 0) {
            dc[i] = 2*sqrt(d[i]*d[i]/4 - (z[i]-zpos)*(z[i]-zpos));
            zc[i] = 1;  // nuclius intersects section
        } else
            zc[i] = -1;  // // nuclius does not intersect section
    }
}

/**
  * checks if a generated nuclius is valid (does not fall inside pre-existing particle)
  * x,y,z: array of centre coordinates of particles
  * gap: gap between the generated nuclius and centre of any particle  d0: initial diameter nuclius
  * Returns 1 if valid nuclius otherwise 0
*/
int validNuclius(int x[], int y[], int z[], float d[], int xc, int yc, int zc, int gap, int d0, int nNuclii)
{
    int i;
    for (i=0;i<nNuclii;i++)
        if ((xc-x[i])*(xc-x[i]) + (yc-y[i])*(yc-y[i]) + (zc-z[i])*(zc-z[i]) < d[i]*d[i]/4 + gap*gap + d0)
            return 0;  // false
    return 1;  // true
}

/**  generates section at each iteration in the 2D array (img)
  *  Returns number of non-zero pixels in img
*/
int generateSection(uint16_t img[], int x[], int y[], float dc[], int zc[], int gray[], int nNuclii, int np)
{
    int i;

    for (i=0;i<nNuclii;i++) {
        if (zc[i] > 0) {
            if (gray[i] > 1000) {
                fprintf(fpDebug, "i = %d, gray[i] = %d\n", i, gray[i]);
            }
            np = drawDisk(img, dc[i]/2, x[i], y[i], gray[i], np);
        }
    }
    return np;   // returns total number of pixels assigned gray values
}

/**
  * generates nuclii upto a maximum given by nucleationRate
  * Returns total nuclii generated so far
*/
int generateNuclii(int x[], int y[], int z[], float d[], int zc[], int gray[], int gap, int d0, int nNuclii, int nucleationRate) {
    int i;
    int crd[3];

    for (i=0;i<nucleationRate;i++) {
        if (nNuclii > MAXNUCLII-2)
            return nNuclii;
        crd[0] = round(LL*((double)rand() / RAND_MAX));
        crd[1] = round(W*((double)rand() / RAND_MAX));
        crd[2] = round(HEIGHT*((double)rand() / RAND_MAX));
        if (validNuclius(x, y, z, d, crd[0], crd[1], crd[2], gap, d0, nNuclii)) {
            x[nNuclii] = crd[0];
            y[nNuclii] = crd[1];
            z[nNuclii] = crd[2];
            d[nNuclii] = d0;
            zc[nNuclii] = -1;
//            gray[nNuclii] = 5+round(10000*((double)rand() / RAND_MAX));
            gray[nNuclii] = nNuclii + 1;
            nNuclii ++;
        }
    }
    return nNuclii;
}

/** Generates a number of nuclii and increments all diameters by growthRate
  * Returns total number of nuclii generated so far
*/
int nucleation_growth(int n, int x[], int y[], int z[], float d[], int zc[], int gray[], int gap, int d0, int nNuclii, int nucleationRate, float growthRate) {
    int i;

    for (i=0;i<n;i++) {
        nNuclii = generateNuclii(x, y, z, d, zc, gray, gap, d0, nNuclii, nucleationRate);
        incrementDia(d, nNuclii, growthRate);
   }
    return nNuclii;
}

/** Re-maps individual grain pixels with sequential numbers (1, 2, 3, ...)
  * Returns the number of grains or on error returns a negative number
*/
int reMapGrains(uint16_t img[], int size, int nNuclii, int randomizeGrayValues)
{
    int i, j, n = 0;
    uint16_t sw;
    uint16_t *map, *randomMap;

    map = (uint16_t *) malloc((nNuclii+1)*sizeof(uint16_t));
    if (map == NULL) {
        fprintf(fpDebug, "Error: Unable to allocate memory to map array\n");
        return -1;
    }
    for (i=0;i<=nNuclii;i++)
        map[i] = 0;
    for (i=0;i<size;i++) {
        if (img[i] > nNuclii || img[i] == 0) {
            fprintf(fpDebug, "Error in selecting gray values: nNuclii = %d, i = %d, img[i] = %d\n", nNuclii, i, (int) img[i]);
            return -2;
        }
        if (map[img[i]] == 0) {
            n++;
            map[img[i]] = n;
        }
    }
//    for (i=0;i<=nNuclii;i++)
//        fprintf(fpDebug, "i = %d, map[i] = %d\n", i, (int) map[i]);
    if (randomizeGrayValues != 0) {
        randomMap = (uint16_t *) malloc((n+1)*sizeof(uint16_t));        // randomly shuffle gray values
        if (randomMap == NULL) {
            fprintf(fpDebug, "Error: Unable to allocate memory to randomMap array\n");
            return -1;
        }
        for (i=0;i<=n;i++)
            randomMap[i] = i;
        for (i=n;i>1;i--) {
            j = 1 + round((n-1)*((double)rand() / RAND_MAX));
//            fprintf(fpDebug, "Shuffling: i = %d, j = %d\n", i, j);
            sw = randomMap[i];
            randomMap[i] = randomMap[j];
            randomMap[j] = sw;
        }
//        for (i=0;i<=n;i++)
//            fprintf(fpDebug, "i = %d, randomMap[i] = %d\n", i, (int) randomMap[i]);
        for (i=0;i<size;i++) {
            if (map[img[i]] == 0 || map[img[i]] > n) {
                fprintf(fpDebug, "Error: i = %d, img[i] = %d, map[img[i]] = %d", i, (int) img[i], (int) map[img[i]]);
                return -3;
            }
            img[i] = randomMap[map[img[i]]];
        }
    } else {
        for (i=0;i<size;i++)
            img[i] = map[img[i]];
    }
    free(map);
    return n;
}

/** Generates a 2D section of grains
  * Returns the number of grains in the section
*/
extern "C" int generateStructure(uint16_t img[], int length, int width, int height, int nucleationRate, float growthRate, float *avramiExponent, int randomizeGrayValues)
{
    printf("starting...\n");

    int gap = 50;
    int nNuclii = 0;          // keeps count of number of nuclii generated
    int d0 = 0.0;
    int i,n, np=0, zpos, ng;
    float vf =0 ;  // volume fraction transformed
    float xx,yy, Sxy = 0, Sx = 0, Sy = 0, Sx2 = 0; // regression terms

    float d[MAXNUCLII]; // diameter array
    int x[MAXNUCLII]; // x,y,z: coordinates of centre (or position) of nuclii
    int y[MAXNUCLII];
    int z[MAXNUCLII];
    int zc[MAXNUCLII];
    float dc[MAXNUCLII]; // diameter of profiles of disks
    int gray[MAXNUCLII];  // gray value of nuclii
    int j;
    FILE *fp;
// Set the Global Variables
    LL = length;
    W = width;
    HEIGHT = height;
    S = ((LL+1)*(W+1));

    //srand(1);       // COMMENT IT TO ENABLE RANDOMIZE THE STRUCTURE
    zpos = height/2;
    rsection(d, dc, z, zc, zpos, nNuclii);
    np = 0;
    i = 0;
    n = 0;
    fpDebug = fopen("PlysimDebug.txt", "w");
    fpAvrami = fopen("PlysimAvrami.csv", "w");
    fprintf(fpAvrami, "t, vf\n");
    while (np < S) {  // repeat until no non-zero pixel remains in the image array (img)
        nNuclii = nucleation_growth(1, x, y, z, d, zc, gray, gap, d0, nNuclii, nucleationRate, growthRate);
        rsection(d, dc, z, zc, zpos, nNuclii);
        np = generateSection(img, x, y, dc, zc, gray, nNuclii, np);
        i++;

        vf = (float) np/S;
        if (vf > 0 && vf < 1) {
            fprintf(fpAvrami, "%d,%f\n", i, vf);
            xx = log(i);
            yy = log(-log(1-vf));
            Sx += xx; Sy += yy; Sxy += xx*yy; Sx2 += xx*xx;
            n++;
        }
    }
    *avramiExponent = (n*Sxy - Sx*Sy)/(n*Sx2 - Sx*Sx);          // slope of the log(-log(1-X)) vs log(time)
    ng = reMapGrains(img, S, nNuclii, randomizeGrayValues);
    fprintf(fpDebug, "length, width, height :: %d, %d, %d\nnucleationRate, growthRate :: %d, %f\nng, nNuclii :: %d, %d\n", length, width, height, nucleationRate, growthRate, ng, nNuclii);
    fclose(fpDebug);
    fclose(fpAvrami);
    fp = fopen("img.csv", "w");  // create ',' separated image data (csv format)
    for (i=0;i<=LL;i++) {
        for (j=0;j<=W;j++) {
            fprintf(fp, "%u,", (uint16_t) img[i*(W+1)+j]);
        }
        fprintf(fp, "\n");
    }
    fclose(fp);
    return ng;
}
// Forward declaration of your function
extern "C" int generateStructure(uint16_t img[], int length, int width, int height,
                                 int nucleationRate, float growthRate, float *avramiExponent,
                                 int randomizeGrayValues);

// Wrapper function to expose to Python
static PyObject* py_generateStructure(PyObject* self, PyObject* args) {
    PyObject* img_obj;
    int length, width, height, nucleationRate, randomizeGrayValues;
    float growthRate;

    if (!PyArg_ParseTuple(args, "Oiiiiif", &img_obj, &length, &width, &height,
                          &nucleationRate, &randomizeGrayValues, &growthRate)) {
        return NULL;
    }

    // Convert the input object to a NumPy array
    PyArrayObject* img_array = (PyArrayObject*) PyArray_FROM_OTF(img_obj, NPY_UINT16, NPY_IN_ARRAY);
    if (img_array == NULL) {
        return NULL;
    }

    // Get a pointer to the data as a C-type array
    uint16_t* img = (uint16_t*) PyArray_DATA(img_array);

    float avramiExponent;
    int result = generateStructure(img, length, width, height, nucleationRate,
                                   growthRate, &avramiExponent, randomizeGrayValues);

    Py_DECREF(img_array);

    // Return the result and avramiExponent as a Python tuple
    return Py_BuildValue("if", result, avramiExponent);
}

// Define the methods of your module
static PyMethodDef LibPolySimMethods[] = {
    {"generateStructure", py_generateStructure, METH_VARARGS, "Generate a polycrystalline structure."},
    {NULL, NULL, 0, NULL}
};

// Define the module
static struct PyModuleDef libpolySimModule = {
    PyModuleDef_HEAD_INIT,
    "libpolySim",     // Name of the module
    NULL,             // Module documentation (may be NULL)
    -1,               // Size of per-interpreter state of the module
    LibPolySimMethods
};

// Initialization function
PyMODINIT_FUNC PyInit_libpolySim(void) {
    import_array();  // Initialize NumPy API
    return PyModule_Create(&libpolySimModule);
}
