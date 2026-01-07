clear; clf; close all;

% --- Coordenadas y parámetros ---
txLat = 6.2875; txLon = -73.1467;
rxLat = 6.4784847569495865; rxLon = -72.97264000422128;
freq = 540e6;               % Hz
c = 3e8;                    % m/s

% --- Iniciales de altura (valores semilla) ---
txAntennaHeight = 80;   % m sobre terreno
rxAntennaHeight = 60;   % m sobre terreno

% --- Modelo Longley-Rice ---
groundCond = 0.02; groundPerm = 15; refractivity = 301;
climateZone = "continental-temperate";
timeVar = 0.5; sitVar = 0.5;
pm = propagationModel("longley-rice", ...
    "GroundConductivity", groundCond, ...
    "GroundPermittivity", groundPerm, ...
    "AtmosphericRefractivity", refractivity, ...
    "ClimateZone", climateZone, ...
    "TimeVariabilityTolerance", timeVar, ...
    "SituationVariabilityTolerance", sitVar);

% --- Crear sitios (usa las alturas iniciales) ---
tx = txsite("Name","Tx_Remote","Latitude",txLat,"Longitude",txLon, ...
            "TransmitterFrequency",freq,"AntennaHeight",txAntennaHeight);
rx = rxsite("Name","Hospital_Mogotes","Latitude",rxLat,"Longitude",rxLon, ...
            "AntennaHeight",rxAntennaHeight);

% --- Distancia entre puntos (Haversine para robustez) ---
R = 6371000; % radio tierra en m
lat1 = deg2rad(txLat); lon1 = deg2rad(txLon);
lat2 = deg2rad(rxLat); lon2 = deg2rad(rxLon);
dlat = lat2 - lat1; dlon = lon2 - lon1;
a = sin(dlat/2).^2 + cos(lat1).*cos(lat2).*sin(dlon/2).^2;
dist_m = 2*R*asin(sqrt(a));
fprintf('Distancia Tx–Rx = %.2f m (%.3f km)\n', dist_m, dist_m/1000);

% --- Elevación del terreno en los sitios (m MSL) ---
try
    z_tx = elevation(tx);
    z_rx = elevation(rx);
    fprintf('Elevación Tx = %.2f m MSL, Rx = %.2f m MSL\n', z_tx, z_rx);
    fprintf('Altura efectiva (Tx): %.2f m MSL, (Rx): %.2f m MSL\n', z_tx + tx.AntennaHeight, z_rx + rx.AntennaHeight);
catch
    warning('La función elevation falló (quizá no tienes acceso a datos). Sigue con tests de altura local.');
end

% --- Comprobar LOS y perfil ---
try
    figure(1); clf;
    los(tx, rx); % abre site viewer o dibuja visibilidad
catch
    warning('los(tx,rx) falló en este entorno gráfico, continúa con pathloss.');
end

% --- Cálculo simple inicial de Path Loss y FSPL de referencia ---
[pl_dB, info] = pathloss(pm, rx, tx);
fspl_dB = 20*log10(4*pi*dist_m*freq/c);
fprintf('PL Longley-Rice (mediana): %.2f dB\n', pl_dB);
fprintf('FSPL a %.2f km: %.2f dB\n', dist_m/1000, fspl_dB);
disp('Campos en info:'); disp(fieldnames(info));

% --- Barrido de alturas (variando RX manteniendo TX fijo) ---
rx_heights = [1 2 5 10 20 40 80 150];
pl_rx = zeros(size(rx_heights));
for k = 1:length(rx_heights)
    rx.AntennaHeight = rx_heights(k);   % REASIGNAR propiedad del objeto
    pl_rx(k) = pathloss(pm, rx, tx);
end

% --- Barrido de alturas (variando TX manteniendo RX fijo) ---
tx_heights = [1 2 5 10 20 40 80 150];
pl_tx = zeros(size(tx_heights));
% guardar rx fix, luego restaurar si es necesario
for k = 1:length(tx_heights)
    tx.AntennaHeight = tx_heights(k);
    pl_tx(k) = pathloss(pm, rx, tx);
end

% --- Graficar resultados ---
figure(2); clf;
subplot(1,2,1);
plot(rx_heights, pl_rx, '-o','LineWidth',1.5);
xlabel('Rx antenna height (m)'); ylabel('Path loss (dB)');
title('Sensibilidad de Path Loss a altura Rx'); grid on;

subplot(1,2,2);
plot(tx_heights, pl_tx, '-o','LineWidth',1.5);
xlabel('Tx antenna height (m)'); ylabel('Path loss (dB)');
title('Sensibilidad de Path Loss a altura Tx'); grid on;

% --- Guardar resultados básicos ---
T = table(pl_dB, fspl_dB, tx.AntennaHeight, rx.AntennaHeight, dist_m);
writetable(T, "LR_result_mogotes_debug.csv");

% Mensaje final explicativo
fprintf('\nHecho. Revisa las gráficas. Si las curvas están casi planas,\nsignifica que el enlace está en buena LOS y la variación de altura no cambia mucho la pérdida.\nSi ves caídas fuertes en PL al aumentar la altura, entonces habías tenido alguna obstrucción por terreno.\n');
