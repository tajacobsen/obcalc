/* Copyright (C) 2010 by Troels Kofoed Jacobsen
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation version 2 of the License.
 * 
 * This program is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
 * more details.
 */
 #include "obwrap.h"

int test()
{
    return 1;
}

int vvv3_len(std::vector< std::vector< OpenBabel::vector3 > > f)
{
    return f.size();
}

double forces_ni(OpenBabel::OBMol * mol, int atom, int dim)
{
    OpenBabel::OBConformerData *cd = 
        static_cast<OpenBabel::OBConformerData*>(mol->GetData(OpenBabel::OBGenericDataType::ConformerData)); 

    std::vector< std::vector < OpenBabel::vector3 > > f = cd->GetForces();
   
    switch (dim)
    {
        case 0: return f[0][atom].x();
        case 1: return f[0][atom].y();
        case 2: return f[0][atom].z();
        default: return 0.0;
    }
}

