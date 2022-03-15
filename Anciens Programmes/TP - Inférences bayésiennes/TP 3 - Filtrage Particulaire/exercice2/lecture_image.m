function [im,filenames,T,SEQUENCE]=lecture_image

SEQUENCE = './sequence3/' ;
START = 1 ;
% charge le nom des images de la s´equence
filenames = dir([SEQUENCE '*.bmp']) ;
%filenames = sort(filenames.name) ;
T = length(filenames) ;
% charge la premiere image dans ’im’
tt = 1 ;
im = imread([SEQUENCE filenames(tt).name]) ;
% affiche ’im’
fig = figure;
set(fig,'Units','Normalized','Position',[0 0 1 1]);
set(gcf, 'DoubleBuffer', 'on') ;
imagesc(im) ;
hold on