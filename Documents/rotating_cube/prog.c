#include <stdio.h>
#include <unistd.h>
#include <windows.h>

int main(int argc, char**argv) {
  int i, j;
  fprintf(stderr, "0%%       50%%       100%%\n");
  fprintf(stderr, "+---------+---------+\n");
  for (i = 0; i <= 100; i++) {
    for (j = 0; j < i / 5 + 1; j++) {
      fprintf(stderr, "#");
    }
    fprintf(stderr, "\n");
    fprintf(stderr, "%3d%%\n", i);
    usleep(100000);
    fprintf(stderr, "\x1b[2A");
    printf("\x1b[33m");
  }
  fprintf(stderr, "\n\nfinish!\n");
  return 0;
}