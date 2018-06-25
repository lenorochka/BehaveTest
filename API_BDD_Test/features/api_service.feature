Feature: Автоматизированные тесты API авторизации Дом.ру ТВ (http://tv.domru.ru) и получения расписания.
	Scenario: Успешность авторизации при передаче корректных данных
		Given domru-api-service
		Then "auth" result is successful
		Then "auth" result is match to schema "schema_auth"

	Scenario: Успешность получения расписания при передаче корректных данных
		Given domru-api-service
		and schedule for channel "1" max "5" elements from time "1497861974"
		Then "auth" result is successful
		Then "schedule" result is successful
		Then "schedule" result is match to schema "schema_schedule"

	Scenario: Ошибка авторизации при неправильных параметрах
		Given domru-api-service with missing argument
		Then "auth" result is failed and error is "missing argument"

	Scenario: Ошибка авторизации с ошибочным клиентом
		Given domru-api-service with params="client_id=--er_ottweb_device&timestamp=1497861974&device_id=123"
		Then "auth" result is failed and error is "invalid client"

	Scenario: Ошибка авторизации с неправильным аргументом timestamp
		Given domru-api-service with params="client_id=er_ottweb_device&timestamp=ff&device_id=123"
		Then "auth" result is failed and error is "invalid argument"
		Then "auth" result error contains "arguments" equals "timestamp"

	Scenario: Ошибка авторизации без аргумента device_id
		Given domru-api-service with params="client_id=er_ottweb_device&timestamp=1497861974"
		Then "auth" result is failed and error is "missing argument"
		Then "auth" result error contains "arguments" equals "device_id"

	Scenario: Ошибка получения расписания с ошибочным токеном
		Given domru-api-service
		Given schedule for channel with wrong token
		Then "schedule" result is failed and error is "no valid token"

	Scenario: Ошибка получения расписания при передаче несуществующего номера канала (не должно ли вызвать ошибку?)
		Given domru-api-service
		and schedule for channel "99999999999" max "5" elements from time "1497861974"
		Then "auth" result is successful
		Then "schedule" result is successful

	Scenario: Ошибка получения расписания при передаче ошибочного времени
		Given domru-api-service
		and schedule for channel "1" max "5" elements from time "gg"
		Then "auth" result is successful
		Then "schedule" result return status 404