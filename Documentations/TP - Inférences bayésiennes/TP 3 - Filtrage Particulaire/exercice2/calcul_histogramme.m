function [littleim,Cmap,histoRef]=calcul_histogramme(im,zoneAT,Nb)

%Nb=size(im,1)*size(im,2)*size(im,3);
littleim = imcrop(im,zoneAT(1:4)) ;
[littleim, Cmap] = rgb2ind(littleim,Nb,'nodither') ;
histoRef = imhist(littleim, Cmap) ;
histoRef = histoRef / norm(histoRef) ;