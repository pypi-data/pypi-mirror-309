//===----------------------------------------------------------------------===//
//
//        OpenSees - Open System for Earthquake Engineering Simulation    
//
//===----------------------------------------------------------------------===//
//
// Description: This file contains the class implementation of FrameSolidSection3d.
//
// Adapted from NDFiberSection3d
//
// Written: MHS
// Created: 2012
//
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include <Channel.h>
#include <Vector.h>
#include <VectorND.h>
#include <Matrix.h>
#include <MatrixND.h>
#include <classTags.h>
#include <FrameSolidSection3d.h>
#include <ID.h>
#include <FEM_ObjectBroker.h>
#include <Information.h>
#include <SensitiveResponse.h>
typedef SensitiveResponse<FrameSection> SectionResponse;
#include <NDMaterial.h>
#include <Parameter.h>
#include <elementAPI.h>

#define SEC_TAG_FrameSolidSection3d 0

using OpenSees::VectorND;
using OpenSees::MatrixND;

ID FrameSolidSection3d::code(6);

FrameSolidSection3d::FrameSolidSection3d(int tag, int num, double a, bool compCentroid): 
    FrameSection(tag, SEC_TAG_FrameSolidSection3d),
    numFibers(0), sizeFibers(num), theMaterials(0), matData(0),
    Abar(0.0), QyBar(0.0), QzBar(0.0), yBar(0.0), zBar(0.0), computeCentroid(compCentroid),
    alpha(a), e(6), s(0), ks(0), 
    parameterID(0), dedh(6)
{
    if (sizeFibers != 0) {
        theMaterials = new NDMaterial *[sizeFibers]{};
        matData = new double [sizeFibers*3]{};
    }

    s = new Vector(sData, 6);
    ks = new Matrix(kData, 6, 6);

    for (int i = 0; i < 6; i++)
        sData[i] = 0.0;

    for (int i = 0; i < 6*6; i++)
        kData[i] = 0.0;

    code(0) = SECTION_RESPONSE_P;
    code(1) = SECTION_RESPONSE_MZ;
    code(2) = SECTION_RESPONSE_MY;
    code(3) = SECTION_RESPONSE_VY;
    code(4) = SECTION_RESPONSE_VZ;
    code(5) = SECTION_RESPONSE_T;
}

// constructor for blank object that recvSelf needs to be invoked upon
FrameSolidSection3d::FrameSolidSection3d():
  FrameSection(0, SEC_TAG_FrameSolidSection3d),
  numFibers(0), sizeFibers(0), theMaterials(0), matData(0),
  Abar(0.0), QyBar(0.0), QzBar(0.0), yBar(0.0), zBar(0.0), computeCentroid(true),
  alpha(1.0), e(6), s(0), ks(0),
  parameterID(0), dedh(6)
{
  s = new Vector(sData, 6);
  ks = new Matrix(kData, 6, 6);

  for (int i = 0; i < 6; i++)
    sData[i] = 0.0;

  for (int i = 0; i < 6*6; i++)
    kData[i] = 0.0;

  code(0) = SECTION_RESPONSE_P;
  code(1) = SECTION_RESPONSE_MZ;
  code(2) = SECTION_RESPONSE_MY;
  code(3) = SECTION_RESPONSE_VY;
  code(4) = SECTION_RESPONSE_VZ;
  code(5) = SECTION_RESPONSE_T;
}

int
FrameSolidSection3d::addFiber(NDMaterial& theMat, const double Area, const double yLoc, const double zLoc)
{
  // need to create larger arrays
  if(numFibers == sizeFibers) {
      int newSize = 2*sizeFibers;
      NDMaterial **newArray = new NDMaterial *[newSize]; 
      double *newMatData = new double [3 * newSize];

      // copy the old pointers and data
      for (int i = 0; i < numFibers; i++) {
          newArray[i] = theMaterials[i];
          newMatData[3*i] = matData[3*i];
          newMatData[3*i+1] = matData[3*i+1];
          newMatData[3*i+2] = matData[3*i+2];
      }

      // initialize new memory
      for (int i = numFibers; i < newSize; i++) {
          newArray[i]       = 0;
          newMatData[3*i]   = 0.0;
          newMatData[3*i+1] = 0.0;
          newMatData[3*i+2] = 0.0;
      }

      sizeFibers = newSize;

      // set new memory
      if (theMaterials != 0) {
          delete [] theMaterials;
          delete [] matData;
      }

      theMaterials = newArray;
      matData = newMatData;
  }

  // set the new pointers and data
  matData[numFibers*3]    = yLoc;
  matData[numFibers*3+1]  = zLoc;
  matData[numFibers*3+2]  = Area;
  theMaterials[numFibers] = theMat.getCopy("BeamFiber");

  if (theMaterials[numFibers] == 0) {
    opserr <<"FrameSolidSection3d::addFiber -- failed to get copy of a Material\n";
    return -1;
  }

  numFibers++;

  // Recompute centroid
  if (computeCentroid) {
    Abar  += Area;
    QzBar += yLoc*Area;
    QyBar += zLoc*Area;
    
    yBar = QzBar/Abar;
    zBar = QyBar/Abar;
  }
  
  return 0;
}


// destructor:
FrameSolidSection3d::~FrameSolidSection3d()
{
  if (theMaterials != 0) {
    for (int i = 0; i < numFibers; i++)
      if (theMaterials[i] != 0)
        delete theMaterials[i];
      
    delete [] theMaterials;
  }

  if (matData != 0)
    delete [] matData;

  if (s != 0)
    delete s;

  if (ks != 0)
    delete ks;

}

//      0  5 4       1       2  3
// a = [1 -y z       0       0  0
//      0  0 0 sqrt(a)       0 -z
//      0  0 0       0 sqrt(a)  y]
int
FrameSolidSection3d::setTrialSectionDeformation(const Vector &deforms)
{
  e = deforms;

  s->Zero();
  ks->Zero();

  double e0 = deforms(0),
         e1 = deforms(1),
         e2 = deforms(2),
         e3 = deforms(3),
         e4 = deforms(4),
         e5 = deforms(5);


  double rootAlpha = 1.0;
  if (alpha != 1.0)
    rootAlpha = sqrt(alpha);

  int res = 0;
  for (int i = 0; i < numFibers; i++) {
    NDMaterial *theMat = theMaterials[i];
    const double y  = matData[3*i]   - yBar;
    const double z  = matData[3*i+1] - zBar;
    const double A  = matData[3*i+2];

    // determine material strain and set it
    VectorND<3> eps;
    eps[0] = e0 - y*e1 + z*e2;
    eps[1] = rootAlpha*e3 - z*e5;
    eps[2] = rootAlpha*e4 + y*e5;

    res += theMat->setTrialStrain(eps);
    const Vector &stress  = theMat->getStress();
    const Matrix &tangent = theMat->getTangent();

    double d00 = tangent(0,0)*A;
    double d01 = tangent(0,1)*A;
    double d02 = tangent(0,2)*A;
    double d10 = tangent(1,0)*A;
    double d11 = tangent(1,1)*A;
    double d12 = tangent(1,2)*A;
    double d20 = tangent(2,0)*A;
    double d21 = tangent(2,1)*A;
    double d22 = tangent(2,2)*A;

    Matrix &ksi = *ks;
    Vector &si = *s;

    double y2 = y*y;
    double z2 = z*z;
    double yz = y*z;
    double tmp;
    // Bending terms
    ksi(0,0) +=    d00;
    ksi(5,5) += y2*d00;
    ksi(4,4) += z2*d00;
    tmp = -y*d00;
    ksi(0,5) += tmp;
    ksi(5,0) += tmp;
    tmp = z*d00;
    ksi(0,4) += tmp;
    ksi(4,0) += tmp;
    tmp = -yz*d00;
    ksi(5,4) += tmp;
    ksi(4,5) += tmp;
    
    // Shear terms
    ksi(1,1) += alpha*d11;
    ksi(1,2) += alpha*d12;
    ksi(2,1) += alpha*d21;
    ksi(2,2) += alpha*d22;
    
    // Torsion term
    ksi(3,3) += z2*d11 - yz*(d12+d21) + y2*d22;
    
    // Bending-torsion coupling terms
    tmp = -z*d01 + y*d02;
    ksi(0,3) += tmp;
    ksi(5,3) -= y*tmp;
    ksi(4,3) += z*tmp;
    tmp = -z*d10 + y*d20;
    ksi(3,0) += tmp;
    ksi(3,5) -= y*tmp;
    ksi(3,4) += z*tmp;
    
    // Hit tangent terms with rootAlpha
    d01 *= rootAlpha; d02 *= rootAlpha;
    d10 *= rootAlpha; d11 *= rootAlpha; d12 *= rootAlpha;
    d20 *= rootAlpha; d21 *= rootAlpha; d22 *= rootAlpha;
    
    // Bending-shear coupling terms
    ksi(0,1) += d01;
    ksi(0,2) += d02;
    ksi(5,1) -= y*d01;
    ksi(5,2) -= y*d02;
    ksi(4,1) += z*d01;
    ksi(4,2) += z*d02;
    ksi(1,0) += d10;
    ksi(2,0) += d20;
    ksi(1,5) -= y*d10;
    ksi(2,5) -= y*d20;
    ksi(1,4) += z*d10;
    ksi(2,4) += z*d20;
    
    // Torsion-shear coupling terms
    y2 =  y*d22;
    z2 = -z*d11;
    ksi(3,1) +=  z2 + y*d21;
    ksi(3,2) += -z*d12 + y2;
    ksi(1,3) +=  z2 + y*d12;
    ksi(2,3) += -z*d21 + y2;

    double sig0 = stress(0)*A;
    double sig1 = stress(1)*A;
    double sig2 = stress(2)*A;

    si(0) +=    sig0;
    si(1) += -y*sig0;
    si(2) +=  z*sig0;
    si(3) += rootAlpha*sig1;
    si(4) += rootAlpha*sig2;
    si(5) += -z*sig1 + y*sig2;
  }

  return res;
}

const Vector&
FrameSolidSection3d::getSectionDeformation()
{
  return e;
}

const Matrix&
FrameSolidSection3d::getInitialTangent()
{
  static double kInitial[36];
  static Matrix ki(kInitial, 6, 6);
  ki.Zero();

  static double yLocs[10000];
  static double zLocs[10000];
  static double fiberArea[10000];

  {
    for (int i = 0; i < numFibers; i++) {
      yLocs[i] = matData[3*i];
      zLocs[i] = matData[3*i+1];
      fiberArea[i] = matData[3*i+2];
    }
  }

  double rootAlpha = 1.0;
  if (alpha != 1.0)
    rootAlpha = sqrt(alpha);

  for (int i = 0; i < numFibers; i++) {
    NDMaterial *theMat = theMaterials[i];
    double y = yLocs[i] - yBar;
    double z = zLocs[i] - zBar;
    double A = fiberArea[i];

    double y2 = y*y;
    double z2 = z*z;
    double yz = y*z;
    double tmp;

    const Matrix &tangent = theMat->getInitialTangent();

    double d00 = tangent(0,0)*A;
    double d01 = tangent(0,1)*A;
    double d02 = tangent(0,2)*A;
    double d10 = tangent(1,0)*A;
    double d11 = tangent(1,1)*A;
    double d12 = tangent(1,2)*A;
    double d20 = tangent(2,0)*A;
    double d21 = tangent(2,1)*A;
    double d22 = tangent(2,2)*A;

    // Bending terms
    ki(0,0) += d00;
    ki(1,1) += y2*d00;
    ki(2,2) += z2*d00;
    tmp = -y*d00;
    ki(0,1) += tmp;
    ki(1,0) += tmp;
    tmp = z*d00;
    ki(0,2) += tmp;
    ki(2,0) += tmp;
    tmp = -yz*d00;
    ki(1,2) += tmp;
    ki(2,1) += tmp;
    
    // Shear terms
    ki(3,3) += alpha*d11;
    ki(3,4) += alpha*d12;
    ki(4,3) += alpha*d21;
    ki(4,4) += alpha*d22;
    
    // Torsion term
    ki(5,5) += z2*d11 - yz*(d12+d21) + y2*d22;
    
    // Bending-torsion coupling terms
    tmp = -z*d01 + y*d02;
    ki(0,5) += tmp;
    ki(1,5) -= y*tmp;
    ki(2,5) += z*tmp;
    tmp = -z*d10 + y*d20;
    ki(5,0) += tmp;
    ki(5,1) -= y*tmp;
    ki(5,2) += z*tmp;
    
    // Hit tangent terms with rootAlpha
    d01 *= rootAlpha; d02 *= rootAlpha;
    d10 *= rootAlpha; d11 *= rootAlpha; d12 *= rootAlpha;
    d20 *= rootAlpha; d21 *= rootAlpha; d22 *= rootAlpha;
    
    // Bending-shear coupling terms
    ki(0,3) += d01;
    ki(0,4) += d02;
    ki(1,3) -= y*d01;
    ki(1,4) -= y*d02;
    ki(2,3) += z*d01;
    ki(2,4) += z*d02;
    ki(3,0) += d10;
    ki(4,0) += d20;
    ki(3,1) -= y*d10;
    ki(4,1) -= y*d20;
    ki(3,2) += z*d10;
    ki(4,2) += z*d20;
    
    // Torsion-shear coupling terms
    y2 =  y*d22;
    z2 = -z*d11;
    ki(5,3) +=  z2 + y*d21;
    ki(5,4) += -z*d12 + y2;
    ki(3,5) +=  z2 + y*d12;
    ki(4,5) += -z*d21 + y2;
  }

  return ki;
}

const Matrix&
FrameSolidSection3d::getSectionTangent()
{
  return *ks;
}

const Vector&
FrameSolidSection3d::getStressResultant()
{
  return *s;
}

FrameSection*
FrameSolidSection3d::getFrameCopy()
{
  FrameSolidSection3d *theCopy = new FrameSolidSection3d ();
  theCopy->setTag(this->getTag());

  theCopy->numFibers = numFibers;
  theCopy->sizeFibers = numFibers;

  if (numFibers != 0) {
    theCopy->theMaterials = new NDMaterial *[numFibers]; 
    theCopy->matData = new double [numFibers*3];

    for (int i = 0; i < numFibers; i++) {
      theCopy->matData[i*3] = matData[i*3];
      theCopy->matData[i*3+1] = matData[i*3+1];
      theCopy->matData[i*3+2] = matData[i*3+2];
      theCopy->theMaterials[i] = theMaterials[i]->getCopy("BeamFiber");

      if (theCopy->theMaterials[i] == 0) {
        opserr <<"FrameSolidSection3d::getFrameCopy -- failed to get copy of a Material";
        exit(-1);
      }
    }  
  }

  theCopy->e = e;
  theCopy->QzBar = QzBar;
  theCopy->QyBar = QyBar;
  theCopy->Abar = Abar;
  theCopy->yBar = yBar;
  theCopy->zBar = zBar;
  theCopy->computeCentroid = computeCentroid;
  theCopy->alpha = alpha;
  theCopy->parameterID = parameterID;

  for (int i = 0; i < 6; i++)
    theCopy->sData[i] = sData[i];

  for (int i = 0; i < 6*6; i++)
    theCopy->kData[i] = kData[i];

  return theCopy;
}

const ID&
FrameSolidSection3d::getType()
{
  return code;
}

int
FrameSolidSection3d::getOrder () const
{
  return 6;
}

int
FrameSolidSection3d::commitState()
{
  int err = 0;

  for (int i = 0; i < numFibers; i++)
    err += theMaterials[i]->commitState();

  return err;
}

int
FrameSolidSection3d::revertToLastCommit()
{
  int err = 0;

  ks->Zero();
  s->Zero();

  double rootAlpha = 1.0;
  if (alpha != 1.0)
    rootAlpha = sqrt(alpha);

  for (int i = 0; i < numFibers; i++) {
    NDMaterial *theMat = theMaterials[i];
    const double y  = matData[3*i]   - yBar;
    const double z  = matData[3*i+1] - zBar;
    const double A  = matData[3*i+2];

    double y2 = y*y;
    double z2 = z*z;
    double yz = y*z;
    double tmp;

    // invoke revertToLast on the material
    err += theMat->revertToLastCommit();

    // get material stress & tangent for this strain and determine ks and fs
    const Matrix &tangent = theMat->getTangent();
    const Vector &stress = theMat->getStress();

    double d00 = tangent(0,0)*A;
    double d01 = tangent(0,1)*A;
    double d02 = tangent(0,2)*A;
    double d10 = tangent(1,0)*A;
    double d11 = tangent(1,1)*A;
    double d12 = tangent(1,2)*A;
    double d20 = tangent(2,0)*A;
    double d21 = tangent(2,1)*A;
    double d22 = tangent(2,2)*A;

    Matrix &ksi = *ks;
    Vector &si = *s;

    // Bending terms
    ksi(0,0) += d00;
    ksi(5,5) += y2*d00;
    ksi(4,4) += z2*d00;
    tmp = -y*d00;
    ksi(0,5) += tmp;
    ksi(5,0) += tmp;
    tmp = z*d00;
    ksi(0,4) += tmp;
    ksi(4,0) += tmp;
    tmp = -yz*d00;
    ksi(5,4) += tmp;
    ksi(4,5) += tmp;
    
    // Shear terms
    ksi(1,1) += alpha*d11;
    ksi(1,2) += alpha*d12;
    ksi(2,1) += alpha*d21;
    ksi(2,2) += alpha*d22;
    
    // Torsion term
    ksi(3,3) += z2*d11 - yz*(d12+d21) + y2*d22;
    
    // Bending-torsion coupling terms
    tmp       = -z*d01 + y*d02;
    ksi(0,3) += tmp;
    ksi(5,3) -= y*tmp;
    ksi(4,3) += z*tmp;
    tmp       = -z*d10 + y*d20;
    ksi(3,0) += tmp;
    ksi(3,5) -= y*tmp;
    ksi(3,4) += z*tmp;
    
    // Hit tangent terms with rootAlpha
    d01 *= rootAlpha; d02 *= rootAlpha;
    d10 *= rootAlpha; d11 *= rootAlpha; d12 *= rootAlpha;
    d20 *= rootAlpha; d21 *= rootAlpha; d22 *= rootAlpha;
    
    // Bending-shear coupling terms
    ksi(0,1) += d01;
    ksi(0,2) += d02;
    ksi(5,1) -= y*d01;
    ksi(5,2) -= y*d02;
    ksi(4,1) += z*d01;
    ksi(4,2) += z*d02;
    ksi(1,0) += d10;
    ksi(2,0) += d20;
    ksi(1,5) -= y*d10;
    ksi(2,5) -= y*d20;
    ksi(1,4) += z*d10;
    ksi(2,4) += z*d20;
    
    // Torsion-shear coupling terms
    y2 =  y*d22;
    z2 = -z*d11;
    ksi(3,1) +=  z2 + y*d21;
    ksi(3,2) += -z*d12 + y2;
    ksi(1,3) +=  z2 + y*d12;
    ksi(2,3) += -z*d21 + y2;

    double sig0 = stress(0)*A;
    double sig1 = stress(1)*A;
    double sig2 = stress(2)*A;

    si(0) +=    sig0;
    si(1) += -y*sig0;
    si(2) +=  z*sig0;
    si(3) += rootAlpha*sig1;
    si(4) += rootAlpha*sig2;
    si(5) += -z*sig1 + y*sig2;
  }

  if (alpha != 1.0) {

  }

  return err;
}

int
FrameSolidSection3d::revertToStart()
{
  // revert the fibers to start    
  int err = 0;

  ks->Zero();
  s->Zero();
  

  double rootAlpha = 1.0;
  if (alpha != 1.0)
    rootAlpha = sqrt(alpha);

  for (int i = 0; i < numFibers; i++) {
    NDMaterial *theMat = theMaterials[i];

    double y  = matData[3*i]   - yBar;
    double z  = matData[3*i+1] - zBar;
    double A  = matData[3*i+2];

    double y2 = y*y;
    double z2 = z*z;
    double yz = y*z;
    double tmp;

    // invoke revertToLast on the material
    err += theMat->revertToStart();

    // get material stress & tangent for this strain and determine ks and fs
    const Matrix &tangent = theMat->getTangent();
    const Vector &stress = theMat->getStress();

    double d00 = tangent(0,0)*A;
    double d01 = tangent(0,1)*A;
    double d02 = tangent(0,2)*A;
    double d10 = tangent(1,0)*A;
    double d11 = tangent(1,1)*A;
    double d12 = tangent(1,2)*A;
    double d20 = tangent(2,0)*A;
    double d21 = tangent(2,1)*A;
    double d22 = tangent(2,2)*A;

    Matrix &ksi = *ks;
    Vector &si = *s;

    // Bending terms
    ksi(0,0) += d00;
    ksi(5,5) += y2*d00;
    ksi(4,4) += z2*d00;
    tmp = -y*d00;
    ksi(0,5) += tmp;
    ksi(5,0) += tmp;
    tmp = z*d00;
    ksi(0,4) += tmp;
    ksi(4,0) += tmp;
    tmp = -yz*d00;
    ksi(5,4) += tmp;
    ksi(4,5) += tmp;
    
    // Shear terms
    ksi(1,1) += alpha*d11;
    ksi(1,2) += alpha*d12;
    ksi(2,1) += alpha*d21;
    ksi(2,2) += alpha*d22;
    
    // Torsion term
    ksi(3,3) += z2*d11 - yz*(d12+d21) + y2*d22;
    
    // Bending-torsion coupling terms
    tmp = -z*d01 + y*d02;
    ksi(0,3) += tmp;
    ksi(5,3) -= y*tmp;
    ksi(4,3) += z*tmp;
    tmp = -z*d10 + y*d20;
    ksi(3,0) += tmp;
    ksi(3,5) -= y*tmp;
    ksi(3,4) += z*tmp;
    
    // Hit tangent terms with rootAlpha
    d01 *= rootAlpha; d02 *= rootAlpha;
    d10 *= rootAlpha; d11 *= rootAlpha; d12 *= rootAlpha;
    d20 *= rootAlpha; d21 *= rootAlpha; d22 *= rootAlpha;
    
    // Bending-shear coupling terms
    ksi(0,1) += d01;
    ksi(0,2) += d02;
    ksi(5,1) -= y*d01;
    ksi(5,2) -= y*d02;
    ksi(4,1) += z*d01;
    ksi(4,2) += z*d02;
    ksi(1,0) += d10;
    ksi(2,0) += d20;
    ksi(1,5) -= y*d10;
    ksi(2,5) -= y*d20;
    ksi(1,4) += z*d10;
    ksi(2,4) += z*d20;
    
    // Torsion-shear coupling terms
    y2 =  y*d22;
    z2 = -z*d11;
    ksi(3,1) +=  z2 + y*d21;
    ksi(3,2) += -z*d12 + y2;
    ksi(1,3) +=  z2 + y*d12;
    ksi(2,3) += -z*d21 + y2;

    double sig0 = stress(0)*A;
    double sig1 = stress(1)*A;
    double sig2 = stress(2)*A;

    si(0) += sig0;
    si(1) += -y*sig0;
    si(2) += z*sig0;
    si(3) += rootAlpha*sig1;
    si(4) += rootAlpha*sig2;
    si(5) += -z*sig1 + y*sig2;
  }

  if (alpha != 1.0) {

  }

  return err;
}

int
FrameSolidSection3d::sendSelf(int commitTag, Channel &theChannel)
{
  int res = 0;

  // create an id to send objects tag and numFibers, 
  //     size 3 so no conflict with matData below if just 1 fiber
  static ID data(3);
  data(0) = this->getTag();
  data(1) = numFibers;
  data(2) = computeCentroid ? 1 : 0; // Now the ID data is really 3    
  int dbTag = this->getDbTag();
  res += theChannel.sendID(dbTag, commitTag, data);
  if (res < 0) {
    opserr <<  "FrameSolidSection3d::sendSelf - failed to send ID data\n";
    return res;
  }    

  if (numFibers != 0) {
    
    // create an id containingg classTag and dbTag for each material & send it
    ID materialData(2*numFibers);
    for (int i=0; i<numFibers; i++) {
      NDMaterial *theMat = theMaterials[i];
      materialData(2*i) = theMat->getClassTag();
      int matDbTag = theMat->getDbTag();
      if (matDbTag == 0) {
        matDbTag = theChannel.getDbTag();
        if (matDbTag != 0)
          theMat->setDbTag(matDbTag);
      }
      materialData(2*i+1) = matDbTag;
    }    
    
    res += theChannel.sendID(dbTag, commitTag, materialData);
    if (res < 0) {
      opserr <<  "FrameSolidSection3d::sendSelf - failed to send material data\n";
      return res;
    }    

    // send the fiber data, i.e. area and loc
    Vector fiberData(matData, 3*numFibers);
    res += theChannel.sendVector(dbTag, commitTag, fiberData);
    if (res < 0) {
      opserr <<  "FrameSolidSection3d::sendSelf - failed to send material data\n";
      return res;
    }    

    // now invoke send(0 on all the materials
    for (int j=0; j<numFibers; j++)
      theMaterials[j]->sendSelf(commitTag, theChannel);

  }

  return res;
}

int
FrameSolidSection3d::recvSelf(int commitTag, Channel &theChannel,
                         FEM_ObjectBroker &theBroker)
{
  int res = 0;

  static ID data(3);
  
  int dbTag = this->getDbTag();
  res += theChannel.recvID(dbTag, commitTag, data);
  if (res < 0) {
    opserr <<  "FrameSolidSection3d::recvSelf - failed to recv ID data\n";
    return res;
  }    
  this->setTag(data(0));

  // recv data about materials objects, classTag and dbTag
  if (data(1) != 0) {
    ID materialData(2*data(1));
    res += theChannel.recvID(dbTag, commitTag, materialData);
    if (res < 0) {
      opserr <<  "FrameSolidSection3d::recvSelf - failed to recv material data\n";
      return res;
    }    

    // if current arrays not of correct size, release old and resize
    if (theMaterials == 0 || numFibers != data(1)) {
      // delete old stuff if outa date
      if (theMaterials != 0) {
        for (int i=0; i<numFibers; i++)
          delete theMaterials[i];
        delete [] theMaterials;
        if (matData != 0)
          delete [] matData;
        matData = nullptr;
        theMaterials = nullptr;
      }

      // Create memory to hold material pointers and fiber data
      numFibers  = data(1);
      sizeFibers = data(1);
      if (numFibers != 0) {
        theMaterials = new NDMaterial *[numFibers];

        for (int j=0; j<numFibers; j++)
          theMaterials[j] = nullptr;

        matData = new double [numFibers*2];
      }
    }

    Vector fiberData(matData, 3*numFibers);
    res += theChannel.recvVector(dbTag, commitTag, fiberData);
    if (res < 0) {
      opserr <<  "FrameSolidSection3d::recvSelf - failed to recv material data\n";
      return res;
    }    

    int i;
    for (i=0; i<numFibers; i++) {
      int classTag = materialData(2*i);
      int dbTag = materialData(2*i+1);

      // if material pointed to is blank or not of corrcet type, 
      // release old and create a new one
      if (theMaterials[i] == 0)
        theMaterials[i] = theBroker.getNewNDMaterial(classTag);
      else if (theMaterials[i]->getClassTag() != classTag) {
        delete theMaterials[i];
        theMaterials[i] = theBroker.getNewNDMaterial(classTag);      
      }

      if (theMaterials[i] == 0) {
        opserr <<"FrameSolidSection3d::recvSelf -- failed to allocate double array for material data\n";
        exit(-1);
      }

      theMaterials[i]->setDbTag(dbTag);
      res += theMaterials[i]->recvSelf(commitTag, theChannel, theBroker);
    }

    QzBar = 0.0;
    QyBar = 0.0;
    Abar  = 0.0;
    double yLoc, zLoc, Area;

    computeCentroid = data(2) ? true : false;
    
    // Recompute centroid
    for (i = 0; computeCentroid && i < numFibers; i++) {
      yLoc = matData[3*i];
      zLoc = matData[3*i+1];
      Area = matData[3*i+2];
      Abar  += Area;
      QzBar += yLoc*Area;
      QyBar += zLoc*Area;
    }

    if (computeCentroid) {
      yBar = QzBar/Abar;
      zBar = QyBar/Abar;
    } else {
      yBar = 0.0;
      zBar = 0.0;      
    }
  }    

  return res;
}

void
FrameSolidSection3d::Print(OPS_Stream &s, int flag)
{
  s << "\nFrameSolidSection3d, tag: " << this->getTag() << endln;
  s << "\tSection code: " << code;
  s << "\tNumber of Fibers: " << numFibers << endln;
  s << "\tCentroid (y,z): " << yBar << ' ' << zBar << endln;
  s << "\tShape factor, alpha = " << alpha << endln;

  if (flag == 1) {
    for (int i = 0; i < numFibers; i++) {
      s << "\nLocation (y,z) = " << matData[3*i] << ' ' << matData[3*i+1];
      s << "\nArea = " << matData[3*i+2] << endln;
      theMaterials[i]->Print(s, flag);
    }
  }
}

Response*
FrameSolidSection3d::setResponse(const char **argv, int argc,
                              OPS_Stream &output)
{
  Response *theResponse = nullptr;

  if (argc > 2 && strcmp(argv[0],"fiber") == 0) {

    
    int key = numFibers;
    int passarg = 2;
    
    if (argc <= 3) {                  // fiber number was input directly
      
      key = atoi(argv[1]);
      
    } else if (argc > 4) {  // find fiber closest to coord. with mat tag
      
      int matTag = atoi(argv[3]);
      double yCoord = atof(argv[1]);
      double zCoord = atof(argv[2]);
      double closestDist = 0;
      double ySearch, zSearch, dy, dz;
      double distance;
      int j;
      // Find first fiber with specified material tag
      for (j = 0; j < numFibers; j++) {
        if (matTag == theMaterials[j]->getTag()) {
          ySearch = matData[3*j];
          zSearch = matData[3*j+1];

          dy = ySearch-yCoord;
          dz = zSearch-zCoord;
          closestDist = dy*dy + dz*dz;
          key = j;
          break;
        }
      }
      // Search the remaining fibers
      for ( ; j < numFibers; j++) {
        if (matTag == theMaterials[j]->getTag()) {
          ySearch = matData[3*j];
          zSearch = matData[3*j+1];

          dy = ySearch-yCoord;
          dz = zSearch-zCoord;
          distance = dy*dy + dz*dz;
          if (distance < closestDist) {
            closestDist = distance;
            key = j;
          }
        }
      }
      passarg = 4;
    }
    
    else {                  // fiber near-to coordinate specified
      
      double yCoord = atof(argv[1]);
      double zCoord = atof(argv[2]);
      double closestDist;
      double ySearch, zSearch, dy, dz;
      double distance;
      
      ySearch = matData[0];
      zSearch = matData[1];

      dy = ySearch-yCoord;
      dz = zSearch-zCoord;
      closestDist = dy*dy + dz*dz;
      key = 0;
      for (int j = 1; j < numFibers; j++) {
        ySearch = matData[3*j];
        zSearch = matData[3*j+1];
        dy = ySearch-yCoord;
        dz = zSearch-zCoord;
        distance = dy*dy + dz*dz;
        if (distance < closestDist) {
          closestDist = distance;
          key = j;
        }
      }
      passarg = 3;
    }
    
    if (key < numFibers && key >= 0) {
      output.tag("FiberOutput");
      output.attr("yLoc",matData[3*key]);
      output.attr("zLoc",matData[3*key+1]);
      output.attr("area",matData[3*key+2]);
      
      theResponse = theMaterials[key]->setResponse(&argv[passarg], argc-passarg, output);
      
      output.endTag();
    }

  }

  if (theResponse == nullptr)
    return FrameSection::setResponse(argv, argc, output);

  return theResponse;
}


int 
FrameSolidSection3d::getResponse(int responseID, Information &sectInfo)
{
  // Just call the base class method ... don't need to define
  // this function, but keeping it here just for clarity
  return FrameSection::getResponse(responseID, sectInfo);
}



// AddingSensitivity:BEGIN ////////////////////////////////////
int
FrameSolidSection3d::setParameter(const char **argv, int argc, Parameter &param)
{
  if (argc < 1)
    return -1;

  int result = -1;

  if (strstr(argv[0],"alpha") != 0)
    return param.addObject(1, this);

  // Check if the parameter belongs to the material (only option for now)
  if (strstr(argv[0],"material") != 0) {
    
    if (argc < 3)
      return 0;

    // Get the tag of the material
    int materialTag = atoi(argv[1]);
    
    // Loop over fibers to find the right material
    for (int i = 0; i < numFibers; i++)
      if (materialTag == theMaterials[i]->getTag()) {
        int ok = theMaterials[i]->setParameter(&argv[2], argc-2, param);
        if (ok != -1)
          result = ok;
      }
    return result;
  }
  int ok = 0; 
  for (int i = 0; i < numFibers; i++) {
    ok = theMaterials[i]->setParameter(argv, argc, param);
    if (ok != -1)
      result = ok;
  }
  return result;
}

int
FrameSolidSection3d::updateParameter(int paramID, Information &info)
{
  switch(paramID) {
  case 1:
    alpha = info.theDouble;
    return 0;
  default:
    return -1;
  }
}

int
FrameSolidSection3d::activateParameter(int paramID)
{
  parameterID = paramID;

  return 0;
}

const Vector &
FrameSolidSection3d::getSectionDeformationSensitivity(int gradIndex)
{
  return dedh;
}

const Vector &
FrameSolidSection3d::getStressResultantSensitivity(int gradIndex, bool conditional)
{
  static Vector ds(6);
  
  ds.Zero();
  
  static Vector stress(3);
  static Vector dsigdh(3);
  static Vector sig_dAdh(3);
  static Matrix tangent(3,3);

  static double yLocs[10000];
  static double zLocs[10000];
  static double fiberArea[10000];

  {
    for (int i = 0; i < numFibers; i++) {
      yLocs[i] = matData[3*i];
      zLocs[i] = matData[3*i+1];
      fiberArea[i] = matData[3*i+2];
    }
  }

  static double dydh[10000];
  static double dzdh[10000];
  static double areaDeriv[10000];

  {
    for (int i = 0; i < numFibers; i++) {
      dydh[i] = 0.0;
      dzdh[i] = 0.0;
      areaDeriv[i] = 0.0;
    }
  }
  
  double rootAlpha = 1.0;
  if (alpha != 1.0)
    rootAlpha = sqrt(alpha);

  double drootAlphadh = 0.0;
  if (parameterID == 1)
    drootAlphadh = 0.5/rootAlpha;

  for (int i = 0; i < numFibers; i++) {
    double y = yLocs[i] - yBar;
    double z = zLocs[i] - zBar;
    double A = fiberArea[i];
    
    dsigdh = theMaterials[i]->getStressSensitivity(gradIndex,true);

    ds(0) += dsigdh(0)*A;
    ds(1) += -y*dsigdh(0)*A;
    ds(2) +=  z*dsigdh(0)*A;
    ds(3) += rootAlpha*dsigdh(1)*A;
    ds(4) += rootAlpha*dsigdh(2)*A;
    ds(5) += (-z*dsigdh(1)+y*dsigdh(2))*A;

    if (areaDeriv[i] != 0.0 || dydh[i] != 0.0 ||  dzdh[i] != 0.0 || parameterID == 1)
      stress = theMaterials[i]->getStress();

    if (dydh[i] != 0.0 || dzdh[i] != 0.0 || parameterID == 1)
      tangent = theMaterials[i]->getTangent();

    if (areaDeriv[i] != 0.0) {
      sig_dAdh(0) = stress(0)*areaDeriv[i];
      sig_dAdh(1) = stress(1)*areaDeriv[i];
      sig_dAdh(2) = stress(2)*areaDeriv[i];
      
      ds(0) += sig_dAdh(0);
      ds(1) += -y*sig_dAdh(0);
      ds(2) +=  z*sig_dAdh(0);
      ds(3) += rootAlpha*sig_dAdh(1);
      ds(4) += rootAlpha*sig_dAdh(2);
      ds(5) += -z*sig_dAdh(1)+y*sig_dAdh(2);
    }

    if (dydh[i] != 0.0) {
      ds(1) += -dydh[i] * (stress(0)*A);
      ds(5) +=  dydh[i] * (stress(2)*A);
    }

    if (dzdh[i] != 0.0) {
      ds(2) +=  dzdh[i] * (stress(0)*A);
      ds(5) += -dzdh[i] * (stress(1)*A);
    }

    if (parameterID == 1) {
      ds(3) += drootAlphadh * (stress(1)*A);
      ds(4) += drootAlphadh * (stress(2)*A);
    }

    MatrixND<3,6> as;
    as(0,0) =  1;
    as(0,1) = -y;
    as(0,2) =  z;
    as(1,3) = rootAlpha;
    as(2,4) = rootAlpha;
    as(1,5) = -z;
    as(2,5) =  y;
    
    static Matrix dasdh(3,6);
    dasdh(0,1) = -dydh[i];
    dasdh(0,2) = dzdh[i];
    dasdh(1,3) = drootAlphadh;
    dasdh(2,4) = drootAlphadh;
    dasdh(1,5) = -dzdh[i];
    dasdh(2,5) = dydh[i];
    
    static Matrix tmpMatrix(6,6);
    tmpMatrix.addMatrixTripleProduct(0.0, as, tangent, dasdh, 1.0);
    
    ds.addMatrixVector(1.0, tmpMatrix, e, A);
  }

  return ds;
}

const Matrix &
FrameSolidSection3d::getInitialTangentSensitivity(int gradIndex)
{
  static Matrix dksdh(6,6);
  
  dksdh.Zero();
  /*
  double y, A, dydh, dAdh, tangent, dtangentdh;

  static double fiberLocs[10000];
  static double fiberArea[10000];

  if (sectionIntegr != 0) {
    sectionIntegr->getFiberLocations(numFibers, fiberLocs);
    sectionIntegr->getFiberWeights(numFibers, fiberArea);
  }  
  else {
    for (int i = 0; i < numFibers; i++) {
      fiberLocs[i] = matData[2*i];
      fiberArea[i] = matData[2*i+1];
    }
  }

  static double locsDeriv[10000];
  static double areaDeriv[10000];

  if (sectionIntegr != 0) {
    sectionIntegr->getLocationsDeriv(numFibers, locsDeriv);  
    sectionIntegr->getWeightsDeriv(numFibers, areaDeriv);
  }
  else {
    for (int i = 0; i < numFibers; i++) {
      locsDeriv[i] = 0.0;
      areaDeriv[i] = 0.0;
    }
  }
  
  for (int i = 0; i < numFibers; i++) {
    y = fiberLocs[i] - yBar;
    A = fiberArea[i];
    dydh = locsDeriv[i];
    dAdh = areaDeriv[i];
    
    tangent = theMaterials[i]->getInitialTangent();
    dtangentdh = theMaterials[i]->getInitialTangentSensitivity(gradIndex);

    dksdh(0,0) += dtangentdh*A + tangent*dAdh;

    dksdh(0,1) += -y*(dtangentdh*A+tangent*dAdh) - dydh*(tangent*A);

    dksdh(1,1) += 2*(y*dydh*tangent*A) + y*y*(dtangentdh*A+tangent*dAdh);
  }

  dksdh(1,0) = dksdh(0,1);
  */
  return dksdh;
}

int
FrameSolidSection3d::commitSensitivity(const Vector& defSens,
                                       int gradIndex, int numGrads)
{
  double d0 = defSens(0);
  double d1 = defSens(1);
  double d2 = defSens(2);
  double d3 = defSens(3);
  double d4 = defSens(4);
  double d5 = defSens(5);

  dedh = defSens;

  static double dydh[10000];
  static double dzdh[10000];

  { // TODO
    for (int i = 0; i < numFibers; i++) {
      dydh[i] = 0.0;
      dzdh[i] = 0.0;
    }
  }

  static Vector depsdh(3);

  double rootAlpha = 1.0;
  if (alpha != 1.0)
    rootAlpha = sqrt(alpha);

  double drootAlphadh = 0.0;
  if (parameterID == 1)
    drootAlphadh = 0.5/rootAlpha;

  for (int i = 0; i < numFibers; i++) {
    NDMaterial *theMat = theMaterials[i];
    const double y  = matData[3*i]   - yBar;
    const double z  = matData[3*i+1] - zBar;

    // determine material strain and set it
    depsdh(0) = d0 - y*d1 + z*d2 - dydh[i]*e(1) + dzdh[i]*e(2);
    depsdh(1) = rootAlpha*d3 - z*d5 + drootAlphadh*e(3) - dzdh[i]*e(5);
    depsdh(2) = rootAlpha*d4 + y*d5 + drootAlphadh*e(4) + dydh[i]*e(5);

    theMat->commitSensitivity(depsdh,gradIndex,numGrads);
  }

  return 0;
}
// AddingSensitivity:END ///////////////////////////////////
