

## Scripts developed for the implementation of the PhD Project "Seismic of South-East Asia - Australia collision zone  

The scripts are based on ISC data and FMTOMO software package. The folders of the repo include scripts for different functionalities which are useful for tomography.

1. Convert **ISC-EHB** data to **FMTOMO** (ISC-EHB2FMTOMO)
2. Convert **ISC** data to **NonLinLon** (Lomax 2001) (ISC2NLL)
3. Convert **NonLinLoc** results to **FMTOMO** input (NLL2FMTOMO)
4. Convert **Crust1.0** 3D model to **FMTOMO** reference model (crust1.02FMTOMO)
5. Perform **unsupervised machine learning** using density-based scanning (DBSCAN) on ISC dataset to increase the Signal to Noise ratio (SNR) (dbscanClust)
6. Visualising FMTOMO results in 3D using **Mayavi** and **VTK** (visualisationMayavi)

---

## About "Seismic imaging of SE-Asia - Australia collision zone" project

The aim of the project is to provide a new 3-D model of the crust and upper mantle of SE Asia and Australia collision zone. We determine P and S wave velocity of the subsurface by using travel-time tomography.  High-quality data are provided by frequent earthquakes in the region and inverted for source location, velocity and interface structure. An iterative non-linear inversion approach is followed with the aid of FMTOMO software package which uses Fast Marching Method to solve the forward problem. This new model provides useful information about the geometry and dynamics of the subduction zones for better understanding of the generation of megathrust earthquakes and volcanism, and assessment of related hazard.

---

## About

The codes were developed by [Aristides Zenonos](https://www.linkedin.com/in/ariszenonos) (aristideszenonos@gmail.com)