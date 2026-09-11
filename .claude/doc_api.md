# OpenF1 API - Resumo

Fonte: https://openf1.org/docs/#api-endpoints

A OpenF1 API fornece dados abertos e em tempo real da Formula 1 (telemetria de
carro, cronometragem, pilotos, sessoes, etc). Nao possui nenhuma associacao
oficial com a Formula 1 ou empresas ligadas a ela.

## Informacoes gerais

- **Base URL:** `https://api.openf1.org/v1`
- **Autenticacao:** dados historicos (a partir de 2023) sao gratuitos e nao
  exigem autenticacao. Dados em tempo real (live timing) exigem assinatura
  paga.
- **Filtros:** qualquer atributo retornado pelo endpoint (exceto campos do
  tipo array) pode ser usado como query param para filtrar resultados, por
  exemplo `?driver_number=1&session_key=9159`.
- **Operadores de comparacao:** campos numericos e de data aceitam operadores
  como `>`, `>=`, `<`, `<=` no valor do query param (ex:
  `?date>2023-09-15T13:00:00`).
- **Datas:** aceitam varios formatos, processados via parser flexivel
  (`dateutil.parser.parse`).
- **Exportar como CSV:** basta adicionar `csv=true` na query string.
- **Palavra-chave `latest`:** pode ser usada no lugar de `session_key` ou
  `meeting_key` para obter os dados da sessao/evento mais recente.

## Endpoints principais

| Endpoint | Path | Descricao | Principais parametros |
|---|---|---|---|
| Car Data | `/car_data` | Telemetria do carro (velocidade, RPM, marcha, throttle, brake, DRS) em ~3.7 Hz | `driver_number`, `session_key`, `speed` |
| Drivers Championship | `/championship_drivers` | Classificacao de pilotos no campeonato (apenas corridas, beta) | `session_key`, `driver_number` |
| Teams Championship | `/championship_teams` | Classificacao de equipes no campeonato (apenas corridas, beta) | `session_key`, `team_name` |
| Drivers | `/drivers` | Informacoes dos pilotos participantes de uma sessao | `driver_number`, `session_key` |
| Intervals | `/intervals` | Intervalo de tempo entre pilotos durante a corrida | `session_key`, `interval` |
| Laps | `/laps` | Detalhes de cada volta (tempo, setores, velocidade) | `session_key`, `driver_number`, `lap_number` |
| Location | `/location` | Posicao 3D do carro na pista (~3.7 Hz) | `session_key`, `driver_number`, `date` |
| Meetings | `/meetings` | Informacoes de um evento/fim de semana (GP ou teste) | `year`, `country_name` |
| Overtakes | `/overtakes` | Ultrapassagens e trocas de posicao | `session_key`, `overtaking_driver_number` |
| Pit | `/pit` | Informacoes de pit stop | `session_key`, `stop_duration` |
| Position | `/position` | Mudancas de posicao dos pilotos ao longo da sessao | `meeting_key`, `driver_number`, `position` |
| Race Control | `/race_control` | Bandeiras, incidentes, safety car e outros eventos de controle de prova | `flag`, `driver_number`, `date` |
| Sessions | `/sessions` | Informacoes de treinos, classificacao, sprint e corrida | `country_name`, `session_name`, `year` |
| Session Result | `/session_result` | Resultado final de uma sessao | `session_key`, `position` |
| Starting Grid | `/starting_grid` | Grid de largada apos a classificacao | `session_key`, `position` |
| Stints | `/stints` | Periodos continuos de pilotagem e dados de pneu | `session_key`, `tyre_age_at_start` |
| Team Radio | `/team_radio` | Comunicacoes de radio entre piloto e equipe | `session_key`, `driver_number` |
| Weather | `/weather` | Condicoes da pista, atualizadas a cada 1 minuto | `meeting_key`, `wind_direction`, `track_temperature` |

## Endpoints relevantes para este projeto

O projeto (`src/f1/ingestion/`) consome principalmente:

- `/meetings` -> `MeetingRepository`
- `/sessions` -> `SessionRepository`
- `/laps` -> `LapRepository`
- `/drivers` -> `DriverRepository`
