CREATE TABLE usuario (
    id serial PRIMARY KEY,
    usuario char(20) UNIQUE NOT NULL,
    nombre char(20) NOT NULL,
    cargo char(20) NOT NULL,
    area char(30) NOT NULL,
    password char(72) NOT NULL,
    created_at date DEFAULT current_date NOT NULL,
    updated_at date DEFAULT current_date NOT NULL
);








INSERT INTO usuario (usuario, nombre, cargo, area, password)
VALUES
('felipej', 'felipej', 'medico', 'medicina general', '123'),
('ore', 'ore', 'paciente', 'paciente', '456'),
('felipe', 'felipe', 'admin', 'medicina general', '789');
