
clear; clf; close all;

% --- Coordenadas ---
txLat = 6.465843750912566;    txLon = -72.99195608148587;   % Tx: sitio remoto en Mogotes El medio
rxLat = 6.4784847569495865;    rxLon = -72.97264000422128;   % Rx: ESE Hospital San Pedro Claver


% --- Parámetros físicos ---
freq = 540e6;            % Hz (900 MHz). Cambia a la banda que usarás

%{
Altura de cada antena sobre el terreno local (no sobre el nivel del mar).

Impacto: subir la antena Tx reduce difracción (mejora cobertura), bajar la Rx la empeora. 
En terreno montañoso, cambios de decenas de metros pueden modificar la pérdida en decenas de dB.
%}

txAntennaHeight = 30;    % m sobre terreno
rxAntennaHeight = 10;    % m sobre terreno

% Suelo / atmósfera (valores por defecto razonables)
groundCond = 0.02;       % S/m
groundPerm = 15;         % permitividad relativa
refractivity = 301;      % N-units
climateZone = "continental-temperate";
timeVar = 0.5; sitVar = 0.5;

% --- Modelo Longley-Rice ---
pm = propagationModel("longley-rice", ...
    "GroundConductivity", groundCond, ...
    "GroundPermittivity", groundPerm, ...
    "AtmosphericRefractivity", refractivity, ...
    "ClimateZone", climateZone, ...
    "TimeVariabilityTolerance", timeVar, ...
    "SituationVariabilityTolerance", sitVar);

% --- Crear sitios geográficos ---
tx = txsite("Name","Tx_Remote","Latitude",txLat,"Longitude",txLon, ...
            "TransmitterFrequency",freq,"AntennaHeight",txAntennaHeight);
rx = rxsite("Name","Hospital_Mogotes","Latitude",rxLat,"Longitude",rxLon, ...
            "AntennaHeight",rxAntennaHeight);

% --- Visualización y viewer con terreno global GMTED2010 ---
sv = siteviewer(Terrain="gmted2010", Name="Mogotes Terrain Viewer");
show(tx); show(rx);

% --- Cálculo de pathloss ---

%{
pathloss(pm, rx, tx) ejecuta el modelo ITM/Longley-Rice entre tx y rx con las propiedades en pm.

Salidas:
pl_dB: pérdida total estimada en dB (valor escalar). Ej.: 99.68 dB que ya obtuviste.

info: estructura con datos diagnósticos (perfil, pérdidas parciales, si hay LOS, distancias, etc.).

Interpretación práctica:
Para calcular enlace de potencia: Pr_dBm = Pt_dBm + Gt_dBi + Gr_dBi - pl_dB - Lmisc_dB.

Si pl_dB es muy alto (por ej. >120 dB) y tu Tx tiene baja potencia/antenas sin ganancia, quizá no llegue señal útil.
%}


[pl_dB, info] = pathloss(pm, rx, tx);
fprintf('Pérdida (Longley-Rice, mediana): %.2f dB\n', pl_dB);

% --- Guardar resultado básico ---
T = table(pl_dB, freq, txAntennaHeight, rxAntennaHeight);
writetable(T, "LR_result_mogotes_quick.csv");

% --- Cobertura simple alrededor del Tx (opcional) ---
coverage(tx, pm, MaxRange=10e3, SignalStrengths=-120:-5);
