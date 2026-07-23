#include <SDL.h>
#include <iostream>

const int WIDTH = 800;
const int HEIGHT = 500;

int main(int argc, char* argv[]) {
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        std::cout << "SDL could not initialize! SDL_Error: " << SDL_GetError() << "\n";
        return 1;
    }

    SDL_Window* window = SDL_CreateWindow("Dino: Moon Operation - C++ Native", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, WIDTH, HEIGHT, SDL_WINDOW_SHOWN);
    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);

    bool running = true;
    SDL_Event e;
    
    // Player specs
    float playerX = 80;
    float playerY = 380;
    float playerVy = 0;
    bool onGround = true;

    while (running) {
        while (SDL_PollEvent(&e) != 0) {
            if (e.type == SDL_QUIT) {
                running = false;
            } else if (e.type == SDL_KEYDOWN) {
                if ((e.key.keysym.sym == SDLK_SPACE || e.key.keysym.sym == SDLK_UP) && onGround) {
                    playerVy = -10.0f;
                    onGround = false;
                }
            }
        }

        // Physics update
        playerVy += 0.45f;
        playerY += playerVy;
        if (playerY >= 380) {
            playerY = 380;
            playerVy = 0;
            onGround = true;
        }

        // Clear screen (Dark Blue background)
        SDL_SetRenderDrawColor(renderer, 11, 15, 26, 255);
        SDL_RenderClear(renderer);

        // Draw Player (Green Dino)
        SDL_Rect playerRect = { (int)playerX, (int)playerY, 28, 32 };
        SDL_SetRenderDrawColor(renderer, 76, 175, 80, 255);
        SDL_RenderFillRect(renderer, &playerRect);

        SDL_RenderPresent(renderer);
        SDL_Delay(16); // ~60 FPS capping
    }

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
    return 0;
}
