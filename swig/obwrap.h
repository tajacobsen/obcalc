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
#ifndef OBWRAP_H
#define OBWRAP_H

#include <vector>

#include <openbabel/mol.h>
#include <openbabel/math/vector3.h>

int test();

int vvv3_len(std::vector< std::vector< OpenBabel::vector3 > > );

double forces_ni(OpenBabel::OBMol *, int, int);

#endif
