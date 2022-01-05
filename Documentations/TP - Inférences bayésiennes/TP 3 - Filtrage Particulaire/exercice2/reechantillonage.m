function [particules,poids] = reechantillonage(particules,poids)





%nombre de particules
N = max(size((particules)));
c = zeros(1,N);
x_tilde = zeros(size(particules,1),N);

%constriction de la fonction de répartition
c = cumsum(poids);

%ré échantillonnage

for i = 1:N
  j = 1;
  u = rand(1,1);
  while u>c(j)
    j = j+1;
  end;
  %choix de la particule
  x_tilde(:,i)=particules(:,j);
end;

%replacer les particules par les x_tilde
particules = x_tilde;
poids = ones(1,N)/N;
