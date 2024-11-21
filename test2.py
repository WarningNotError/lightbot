import sqlite3

connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# cursor.execute('DROP TABLE IF EXISTS Spec')

# cursor.execute('ALTER TABLE Users RENAME COLUMN email TO message')
# cursor.execute('ALTER TABLE Users RENAME COLUMN age TO time')

# cursor.execute('''
# CREATE TABLE IF NOT EXISTS Spec (
# name TEXT NOT NULL,
# number TEXT NOT NULL PRIMARY KEY,
# matrix TEXT NOT NULL,
# display_size TEXT NOT NULL,
# permission TEXT NOT NULL ,
# pixel_density TEXT NOT NULL,
# aspect_ratio TEXT NOT NULL,
# typical_brightness TEXT NOT NULL ,
# maximum_brightness TEXT NOT NULL,
# contrast_ratio TEXT NOT NULL,
# dynamic_contrast TEXT NOT NULL ,
# response_time TEXT NOT NULL,
# viewing_angles TEXT NOT NULL,
# screen_refresh_rate TEXT NOT NULL ,
# screen_refresh_rate_fhd TEXT NOT NULL,
# eye_strain TEXT NOT NULL,
# number_of_colors TEXT NOT NULL ,
# color_coverage TEXT NOT NULL,
# screen_backlight TEXT NOT NULL,
# display_coverage TEXT NOT NULL,
# video_connectors TEXT NOT NULL,
# HDCP_support TEXT NOT NULL ,
# USB_ports TEXT NOT NULL,
# memory_card TEXT NOT NULL,
# audio_connectors TEXT NOT NULL ,
# sound TEXT NOT NULL,
# webcam TEXT NOT NULL,
# tilt_adjustment TEXT NOT NULL,
# height_adjustment TEXT NOT NULL,
# screen_horizontally TEXT NOT NULL ,
# portrait_mode TEXT NOT NULL,
# VESA_mounting_size TEXT NOT NULL,
# power_unit TEXT NOT NULL ,
# maximum_power_consumption TEXT NOT NULL,
# energy_efficiency_class TEXT NOT NULL,
# body_color TEXT NOT NULL,
# kensington_lock TEXT NOT NULL,
# monitor_dimensions_with_stand TEXT NOT NULL ,
# weight TEXT NOT NULL,
# package_dimensions TEXT NOT NULL ,
# warranty TEXT NOT NULL
# )
# ''')
# cursor.execute('INSERT INTO Zakazi (N_zakaza, SN, Date, Warranty) VALUES (?, ?, ?, ?)', (123, '1', '01.11.2024', '24 мес'))
# cursor.execute('INSERT INTO Zakazi (N_zakaza, SN, Date, Warranty) VALUES (?, ?, ?, ?)', (125, '2', '21.11.2024', '24 мес'))
# cursor.execute('INSERT INTO Zakazi (N_zakaza, SN, Date, Warranty) VALUES (?, ?, ?, ?)', (124, '3', '14.11.2024', '36 мес'))
# cursor.execute('INSERT INTO Zakazi (N_zakaza, SN, Date, Warranty) VALUES (?, ?, ?, ?)', (123, '4', '01.11.2024', '24 мес'))


# cursor.execute('INSERT INTO Spec (name, number, matrix, display_size, permission, pixel_density, aspect_ratio, typical_brightness, maximum_brightness, contrast_ratio, dynamic_contrast, response_time, viewing_angles, screen_refresh_rate, screen_refresh_rate_fhd, eye_strain, number_of_colors, color_coverage, screen_backlight, display_coverage, video_connectors, HDCP_support, USB_ports, memory_card, audio_connectors, sound, webcam, tilt_adjustment, height_adjustment, screen_horizontally, portrait_mode, VESA_mounting_size, power_unit, maximum_power_consumption, energy_efficiency_class, body_color, kensington_lock, monitor_dimensions_with_stand, weight, package_dimensions, warranty) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', ('LightCom V-Plus 24 ПЦВТ.852859.400-04', '6098-4-2023', 'технология IPS', '23,8', '1920 x 1080', '93 ppi', '16:9', '250 кд/м²', '  ', '1000:1', '20 000 000:1', '4 мс', '178°/178°', '75 Гц', '75 Гц', 'есть', '16,7 млн', 'NTSC 72%, sRGB 100%', 'WLED', 'матовое, антибликовое', 'VGA D-Sub, HDMI 1.4', 'есть', 'нет', 'нет', 'Mini-Jack (3.5 мм) вход', 'Стереодинамики', 'нет', '-5°/+20°', 'нет', 'нет', 'нет', '100 x 100 мм', 'внешний', '18 Вт', 'A++', 'черный', 'есть', '538*408*189 мм', '2,66/3,7 кг', '595*460*95 мм', '1 год/до 3-х лет'))


connection.commit()
connection.close()




# (name, number, matrix, display_size, permission, pixel_density, aspect_ratio, typical_brightness, maximum_brightness, contrast_ratio, dynamic_contrast, response_time, viewing_angles, screen_refresh_rate, screen_refresh_rate_fhd, eye_strain, number_of_colors, color_coverage, screen_backlight, display_coverage, video_connectors, HDCP_support, USB_ports, memory_card, audio_connectors, sound, webcam, tilt_adjustment, height_adjustment, screen_horizontally, portrait_mode, VESA_mounting_size, power_unit, maximum_power_consumption, energy_efficiency_class, body_color, kensington_lock, monitor_dimensions_with_stand, weight, eye_strain, package_dimensions, warranty)