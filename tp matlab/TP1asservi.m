close all
clc

num = 10;
dem = [1 -2 10];
G = tf(num,dem)
poles=pole(G)
%zero=zero(G)
figure(1)
pzmap(G)
P=pzmap(G);
grid on;
figure(2)
impulse(G)
grid on;
figure(3)
step(G)
grid on;
figure(4)
t=0: 0.01: 10;
ramp=t;
lsim(G,ramp,t)
grid on;
