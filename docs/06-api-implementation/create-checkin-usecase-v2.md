# CreateCheckInUseCase V2

Actor: Employee

Request DTO:
- week_period

Validaciones:
- Usuario activo
- No existe Check-In para la semana

Evento: CheckInCreated

Pseudocódigo:
validate -> authorize -> create -> commit -> publish_event