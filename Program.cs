using System;
using System.Drawing;
using System.Windows.Forms;

namespace DinoMoonOperation
{
    public class GameForm : Form
    {
        private Timer gameTimer;
        private int playerX = 80, playerY = 380;
        private float playerVy = 0;
        private bool onGround = true;
        private int score = 0;
        private bool godMode = false;

        public GameForm()
        {
            this.Text = "Dino: Moon Operation - C# Native Edition";
            this.Size = new Size(816, 539);
            this.DoubleBuffered = true;
            this.BackColor = Color.FromArgb(11, 15, 26);

            gameTimer = new Timer();
            gameTimer.Interval = 16; // ~60 FPS
            gameTimer.Tick += (sender, e) => { UpdateGame(); Invalidate(); };
            gameTimer.Start();

            this.KeyDown += GameForm_KeyDown;
        }

        private void GameForm_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Space || e.KeyCode == Keys.Up || e.KeyCode == Keys.W)
            {
                if (onGround)
                {
                    playerVy = -12f;
                    onGround = false;
                }
            }
            if (e.KeyCode == Keys.C)
            {
                godMode = !godMode;
                MessageBox.Show(godMode ? "🛡️ GOD MODE ON" : "⚔️ GOD MODE OFF");
            }
        }

        private void UpdateGame()
        {
            playerVy += 0.6f;
            playerY += (int)playerVy;
            if (playerY >= 380)
            {
                playerY = 380;
                playerVy = 0;
                onGround = true;
            }
            score++;
        }

        protected override void OnPaint(PaintEventArgs e)
        {
            base.OnPaint(e);
            Graphics g = e.Graphics;

            // Draw Player (Dino)
            using (Brush playerBrush = new SolidBrush(Color.FromArgb(76, 175, 80)))
            {
                g.FillRectangle(playerBrush, playerX, playerY, 28, 32);
            }

            // Draw HUD
            using (Font font = new Font("Segoe UI", 12))
            using (Brush textBrush = new SolidBrush(Color.FromArgb(183, 208, 240)))
            {
                g.DrawString($"🏆 Score: {score} | C# Engine Active", font, textBrush, 16, 16);
            }
        }

        [STAThread]
        public static void Main()
        {
            Application.EnableVisualStyles();
            Application.Run(new GameForm());
        }
    }
}
