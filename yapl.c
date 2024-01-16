#include <stdio.h>
#include <json_object.h>
#include <json_tokener.h>
#include <json_util.h>
#include <stdlib.h>
#include <sys/types.h>
#include <pwd.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>

int main(int argc, char *argv[]) {
    char *conf_file = getenv("HOME");
    long conf_len;

    if (conf_file == NULL) {
        conf_file = getpwuid(getuid())->pw_dir;
    }

    // strcat(conf_file, "/.config/yapl/yapl.json");
    strcat(conf_file, "/.config/yapl-dev/yapl.json");

    FILE* config = fopen(conf_file, "r");

    if (config == NULL) {
        printf("No such file or directory. Do you forgot to create the config file?");
        return ENOENT;
    }

    // https://stackoverflow.com/questions/174531/how-to-read-the-content-of-a-file-to-a-string-in-c
    fseek(config, 0, SEEK_END);
    conf_len = ftell(config);
    char *conf_raw = malloc(conf_len);
    fseek(config, 0, SEEK_SET);

    // its probably fine to give long type input to int. i have no idea
    if (conf_raw == NULL) {
        printf("Unable to allocate memory");
        return ENOMEM;
    }

    fread(conf_raw, 1, conf_len, config);
    fclose(config);

    json_object *conf_json = json_tokener_parse(conf_raw);
    json_object *programs = json_object_object_get(conf_json, "programs");
    json_type type_raw = json_object_get_type(programs);
    const char *type = json_type_to_name(type_raw);
    printf("%s\n",type);

    json_object_put(conf_json);
    json_object_put(programs);
    json_object_put(conf_json);
    free(conf_raw);

    return 0;
}