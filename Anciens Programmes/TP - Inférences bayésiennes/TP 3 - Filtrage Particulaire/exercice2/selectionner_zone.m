function zoneAT=selectionner_zone

disp('Cliquer 4 points dans l image pour definir la zone a suivre.') ;
zone = zeros(2,4) ;
compteur=1 ;
while(compteur ~= 5)
[x,y,button] = ginput(1) ;
zone(1,compteur) = x ;
zone(2,compteur) = y ;
text(x,y,'X','Color', 'r') ;
compteur = compteur+1 ;
end
newzone = zeros(2,4) ;
newzone(1, :) = sort(zone(1, :)) ;
newzone(2, :) = sort(zone(2, :)) ;
zoneAT = zeros(1,4) ;
zoneAT(1) = newzone(1,1) ;
zoneAT(2) = newzone(2,1) ;
zoneAT(3) = newzone(1,4)-newzone(1,1) ;
zoneAT(4) = newzone(2,4)-newzone(2,1) ;
% affichage du rectangle
rectangle('Position',zoneAT,'EdgeColor','r','LineWidth',3) ;

