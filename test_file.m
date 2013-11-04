clear all;
close all;
clc;
CleanStart;

XYZ = zeros(4,3)
CON = zeros(4,2)

%0
XYZ(1,:) = [12.50522514426531,14.98506778225189,0.0];
XYZ(2,:) = [17.40213026214611,19.94608922194742,0.0];
XYZ(4,:) = [14.97033381881692,12.48790936525268,0.0];
XYZ(3,:) = [20.00048797296532,17.48222619925111,0.0];

CON(1,:) = [1,2];
CON(2,:) = [2,3];
CON(3,:) = [3,4];
CON(4,:) = [4,1];

BOUN = ones(4,3);
BOUN(1,:) = [1, 1, 1]

[ElemName{1:5}] = deal('Truss');

Model = Create_SimpleModel(XYZ,CON,BOUN,ElemName);
