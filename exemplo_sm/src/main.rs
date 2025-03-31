use eframe::egui;
use rand::Rng;
use std::time::{Duration, Instant};

#[derive(Debug, Clone, Copy, PartialEq)]
enum RobotState {
    Inactive,
    Exploring,
    Chasing,
    AvoidingObstacle,
    ReturningToBase,
}

struct Robot {
    state: RobotState,
    battery_level: f32,
    position: (f32, f32),
    target_position: Option<(f32, f32)>,
    last_state_change: Instant,
    state_duration: Duration,
    obstacle_detected: bool,
    target_detected: bool,
    base_position: (f32, f32),
}

impl Robot {
    fn new() -> Self {
        Self {
            state: RobotState::Inactive,
            battery_level: 100.0,
            position: (50.0, 50.0),
            target_position: None,
            last_state_change: Instant::now(),
            state_duration: Duration::from_secs(0),
            obstacle_detected: false,
            target_detected: false,
            base_position: (50.0, 50.0),
        }
    }

    fn update_state(&mut self) {
        let now = Instant::now();
        let time_in_state = now - self.last_state_change;

        if self.battery_level < 20.0 && self.state != RobotState::ReturningToBase {
            self.transition_to(RobotState::ReturningToBase);
            return;
        }

        match self.state {
            RobotState::Inactive => {}

            RobotState::Exploring => {
                if self.target_detected {
                    self.transition_to(RobotState::Chasing);
                } else if self.obstacle_detected {
                    self.transition_to(RobotState::AvoidingObstacle);
                } else if time_in_state > Duration::from_secs(5) {
                    self.choose_new_direction();
                    self.last_state_change = now;
                }
            }

            RobotState::Chasing => {
                if !self.target_detected {
                    self.transition_to(RobotState::Exploring);
                } else if self.obstacle_detected {
                    self.transition_to(RobotState::AvoidingObstacle);
                }
            }

            RobotState::AvoidingObstacle => {
                if !self.obstacle_detected && time_in_state > Duration::from_secs(1) {
                    if self.target_detected {
                        self.transition_to(RobotState::Chasing);
                    } else {
                        self.transition_to(RobotState::Exploring);
                    }
                }
            }

            RobotState::ReturningToBase => {
                let distance_to_base = ((self.position.0 - self.base_position.0).powi(2)
                    + (self.position.1 - self.base_position.1).powi(2))
                .sqrt();

                if distance_to_base < 10.0 {
                    self.battery_level = 100.0;
                    self.transition_to(RobotState::Exploring);
                } else if self.obstacle_detected {
                    self.transition_to(RobotState::AvoidingObstacle);
                }
            }
        }
    }

    fn transition_to(&mut self, new_state: RobotState) {
        println!("Transição de {:?} para {:?}", self.state, new_state);
        self.state = new_state;
        self.last_state_change = Instant::now();
    }

    fn choose_new_direction(&mut self) {
        let mut rng = rand::thread_rng();
        self.target_position = Some((rng.gen_range(0.0..=100.0), rng.gen_range(0.0..=100.0)));
    }

    fn update_position(&mut self) {
        if let Some(target) = self.target_position {
            let dx = target.0 - self.position.0;
            let dy = target.1 - self.position.1;
            let distance = (dx * dx + dy * dy).sqrt();

            if distance > 1.0 {
                let speed = match self.state {
                    RobotState::Chasing => 1.5,
                    RobotState::ReturningToBase => 1.2,
                    _ => 0.8,
                };

                self.position.0 += (dx / distance) * speed;
                self.position.1 += (dy / distance) * speed;
            } else {
                self.target_position = None;
            }
        }

        self.battery_level -= 0.50;
        if self.battery_level < 0.0 {
            self.battery_level = 0.0;
        }

        let mut rng = rand::thread_rng();
        self.obstacle_detected = rng.gen_bool(0.1);
        self.target_detected = rng.gen_bool(0.15);
    }
}

struct RobotApp {
    robot: Robot,
    last_update: Instant,
}

impl RobotApp {
    fn new() -> Self {
        Self {
            robot: Robot::new(),
            last_update: Instant::now(),
        }
    }
}

impl eframe::App for RobotApp {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        if self.last_update.elapsed() > Duration::from_millis(100) {
            self.robot.update_state();
            self.robot.update_position();
            self.last_update = Instant::now();
        }

        egui::SidePanel::left("control_panel").show(ctx, |ui| {
            ui.heading("Controle do Robô");

            ui.label(format!("Estado: {:?}", self.robot.state));
            ui.label(format!("Bateria: {:.1}%", self.robot.battery_level));
            ui.label(format!(
                "Posição: ({:.1}, {:.1})",
                self.robot.position.0, self.robot.position.1
            ));

            if ui.button("Ligar").clicked() && self.robot.state == RobotState::Inactive {
                self.robot.transition_to(RobotState::Exploring);
                self.robot.choose_new_direction();
            }

            if ui.button("Desligar").clicked() {
                self.robot.transition_to(RobotState::Inactive);
            }

            ui.checkbox(&mut self.robot.obstacle_detected, "Obstáculo Detectado");
            ui.checkbox(&mut self.robot.target_detected, "Alvo Detectado");

            ui.separator();
            ui.label("Legenda:");
            ui.colored_label(egui::Color32::from_gray(100), "Inativo");
            ui.colored_label(egui::Color32::from_rgb(0, 150, 255), "Explorando");
            ui.colored_label(egui::Color32::from_rgb(255, 50, 50), "Perseguindo");
            ui.colored_label(egui::Color32::from_rgb(255, 255, 0), "Evitando Obstáculo");
            ui.colored_label(egui::Color32::from_rgb(50, 255, 50), "Retornando à Base");
        });

        egui::CentralPanel::default().show(ctx, |ui| {
            let painter = ui.painter();
            let rect = ui.available_rect_before_wrap();

            painter.rect_filled(rect, 0.0, egui::Color32::from_gray(20));

            let color = match self.robot.state {
                RobotState::Inactive => egui::Color32::from_gray(100),
                RobotState::Exploring => egui::Color32::from_rgb(0, 150, 255),
                RobotState::Chasing => egui::Color32::from_rgb(255, 50, 50),
                RobotState::AvoidingObstacle => egui::Color32::from_rgb(255, 255, 0),
                RobotState::ReturningToBase => egui::Color32::from_rgb(50, 255, 50),
            };

            let robot_x = rect.min.x + rect.width() * (self.robot.position.0 / 100.0);
            let robot_y = rect.min.y + rect.height() * (self.robot.position.1 / 100.0);

            painter.circle_filled(egui::pos2(robot_x, robot_y), 10.0, color);

            let base_x = rect.min.x + rect.width() * (self.robot.base_position.0 / 100.0);
            let base_y = rect.min.y + rect.height() * (self.robot.base_position.1 / 100.0);
            painter.rect_filled(
                egui::Rect::from_center_size(egui::pos2(base_x, base_y), egui::vec2(15.0, 15.0)),
                0.0,
                egui::Color32::from_rgb(150, 150, 150),
            );

            if let Some(target) = self.robot.target_position {
                let target_x = rect.min.x + rect.width() * (target.0 / 100.0);
                let target_y = rect.min.y + rect.height() * (target.1 / 100.0);

                painter.circle_stroke(
                    egui::pos2(target_x, target_y),
                    5.0,
                    egui::Stroke::new(2.0, egui::Color32::from_rgb(255, 255, 255)),
                );
            }
        });
    }
}

fn main() -> eframe::Result<()> {
    let options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default()
            .with_inner_size([800.0, 600.0])
            .with_min_inner_size([400.0, 300.0]),
        ..Default::default()
    };

    eframe::run_native(
        "Simulador de Máquina de Estados para Robô",
        options,
        Box::new(|_cc| Ok(Box::<RobotApp>::new(RobotApp::new()))),
    )
}
