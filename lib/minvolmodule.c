#include <Python.h>
#include "numpy/arrayobject.h"

static PyObject *minvol_getSmallestVols(PyObject *self, PyObject *args) {
    /* input parameters */
    int num_lines;                  // the total number of LOR's in the frame
    PyObject *line_indices;         // (npoints,1) list of ints; ID's of lines along which points lie
    PyObject *point_regions;        // (npoints,1) list of ints; indices into Voronoi regions
    PyObject *regions;              // (nregions,*) list of list of ints; indices into vertices
    PyObject *vertices;             // (nvertices,3) ndarray of doubles; co-ords of vertices
    /* variables used throughout the function */
    /*int line_counter = 0;
    int point_counter = 0;
    int num_points;
    int line_id;*/

    /* Check for correct data types*/
    if (!PyArg_ParseTuple(args, "iOOOO", &num_lines, 
                                         &line_indices, 
                                         &point_regions,
                                         &regions,
                                         &vertices))
        return NULL;
    /* Populate some of the variables */
    //Py_ssize_t py_num_points = PyList_Size(line_indices);
    //PyArg_ParseTuple(&py_num_points, "i", &num_points);
    /* Loop over all the seed points */
//    while(point_counter < num_points)
//    {
//        /*  If the current point lies along the current line, check the
//            size of the corresponding Voronoi volume. Otherwise increment
//            the current line. */    
//        if(line_counter == line_id)
//        {
//            point_counter = point_counter + 1;
//        }
//        else
//        {
//            line_counter = line_counter + 1;
//        }
//    }
    
    return Py_BuildValue("i",1);
}

static struct PyMethodDef minvol_methods[] = {
    {"getSmallestVols", minvol_getSmallestVols, METH_VARARGS, NULL},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC init_minvol(void) {
    PyObject *m = Py_InitModule3("minvol", 
                    minvol_methods,
                   "Gets smallest Voronoi region per line");
    if(m == NULL)
        return;

    import_array();
}