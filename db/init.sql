CREATE TABLE IF NOT EXISTS usuarios (
    id serial PRIMARY KEY,
    usuario varchar(20) UNIQUE NOT NULL,
    nombre varchar(20) NOT NULL,
    cargo varchar(20) NOT NULL,
    area varchar(30) NOT NULL,
    password varchar(72) NOT NULL,  -- Tipo de dato ajustado para flexibilidad
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        ON UPDATE CURRENT_TIMESTAMP  -- Actualiza automáticamente cuando el registro se modifica
);


INSERT INTO usuario (usuario, nombre, cargo, area, password)
VALUES
('felipej', 'felipej', 'medico', 'medicina general', '123'),
('ore', 'ore', 'paciente', 'paciente', '456'),
('felipe', 'felipe', 'admin', 'medicina general', '789')
ON CONFLICT (usuario) DO NOTHING;
