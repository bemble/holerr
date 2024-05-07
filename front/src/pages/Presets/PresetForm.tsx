import { ChangeEvent, useEffect, useRef, useState } from "react";
import {
  Checkbox,
  Chip,
  FormControl,
  FormHelperText,
  Input,
  InputAdornment,
  InputLabel,
  MenuItem,
  Select,
  TextField,
} from "@material-ui/core";
import { useTranslation } from "react-i18next";
import { Preset } from "../../models/presets.type";
import { Autocomplete } from "@material-ui/lab";

type PresetProps = {
  preset: Preset;
  onUpdate: (p: Preset) => void;
};

const ALL_EXTENSIONS = "___all___";

const PresetForm: React.FC<PresetProps> = ({ preset, onUpdate }) => {
  const { t } = useTranslation();
  const didMount = useRef(false);
  const [name, setName] = useState(preset.name || "");
  const [watchDir, setWatchDir] = useState(preset.watch_dir || "");
  const [outputDir, setOutputDir] = useState(preset.output_dir || "");
  const [minFileSizeStr, setMinFileSizeStr] = useState<string>(
    "" + (preset.min_file_size || 0)
  );
  const [minFileSizeUnit, setMinFileSizeUnit] = useState<string>("B");
  const [minFileSize, setMinFileSize] = useState<string | null>(null);
  const [createSubDir, setCreateSubDir] = useState(
    preset.create_sub_dir || false
  );
  const [extensions, setExtensions] = useState(
    preset.file_extensions ? [...preset.file_extensions] : [ALL_EXTENSIONS]
  );

  const cleanMinFileSize = () => {
    setMinFileSizeStr("" + (parseFloat(preset.min_file_size || "") || 0));
    const unit = (preset.min_file_size || "0").replace(/[0-9.]/g, "") || "B";
    console.log(unit);
    setMinFileSizeUnit(unit);
  };

  useEffect(cleanMinFileSize, [preset.min_file_size]);

  useEffect(() => {
    if (minFileSizeStr === "" || minFileSizeStr === "0") {
      setMinFileSize(null);
    } else {
      setMinFileSize(`${minFileSizeStr}${minFileSizeUnit}`);
    }
  }, [minFileSizeStr, minFileSizeUnit]);

  useEffect(() => {
    if (didMount.current) {
      const exts = [...extensions];
      if (exts.indexOf(ALL_EXTENSIONS) >= 0) {
        exts.splice(exts.indexOf(ALL_EXTENSIONS), 1);
      }

      const newPreset = {
        ...preset,
        name,
        watch_dir: watchDir,
        output_dir: outputDir,
        min_file_size: minFileSize,
        create_sub_dir: createSubDir,
        file_extensions: exts.length ? exts : null,
      };
      onUpdate(newPreset);
    } else {
      didMount.current = true;
    }
  }, [name, watchDir, outputDir, minFileSize, createSubDir, extensions]);

  const handleChangeMinFileSizeUnit = (e: ChangeEvent<{ value: unknown }>) => {
    setMinFileSizeUnit(e.target.value as string);
  };

  const handleUpdateExtensions = (e: ChangeEvent<{}>, value: string[]) => {
    if (value.indexOf(ALL_EXTENSIONS) >= 0) {
      value.splice(value.indexOf(ALL_EXTENSIONS), 1);
    }
    setExtensions(value.length === 0 ? [ALL_EXTENSIONS] : value);
  };

  return (
    <>
      <TextField
        label={t("presets.name")}
        defaultValue={name}
        onChange={(e) => setName(e.target.value)}
        fullWidth={true}
      />
      <TextField
        label={t("presets.watch_dir")}
        defaultValue={watchDir}
        onChange={(e) => setWatchDir(e.target.value)}
        fullWidth={true}
      />
      <TextField
        label={t("presets.output_dir")}
        defaultValue={outputDir}
        onChange={(e) => setOutputDir(e.target.value)}
        fullWidth={true}
      />
      <Autocomplete
        multiple
        options={[] as string[]}
        freeSolo
        value={extensions}
        onChange={handleUpdateExtensions}
        renderTags={(value: string[], getTagProps) =>
          value.map((option: string, index: number) =>
            option === ALL_EXTENSIONS ? (
              <Chip variant="outlined" label={t("presets.all")} key={index} />
            ) : (
              <Chip
                variant="outlined"
                label={option}
                {...getTagProps({ index })}
              />
            )
          )
        }
        renderInput={(params) => (
          <TextField
            {...params}
            label={t("presets.file_extensions")}
            fullWidth
          />
        )}
      />
      <FormControl fullWidth={true}>
        <InputLabel htmlFor={`preset-min-file-size-${preset.name}`}>
          {t("presets.min_file_size")}
        </InputLabel>
        <Input
          id={`preset-min-file-size-${preset.name}`}
          value={minFileSizeStr}
          onChange={(e) => setMinFileSizeStr(e.target.value)}
          endAdornment={
            <InputAdornment position="end">
              <Select
                onChange={handleChangeMinFileSizeUnit}
                value={minFileSizeUnit}
              >
                <MenuItem value="TB">{t("units.TB")}</MenuItem>
                <MenuItem value="GB">{t("units.GB")}</MenuItem>
                <MenuItem value="MB">{t("units.MB")}</MenuItem>
                <MenuItem value="KB">{t("units.KB")}</MenuItem>
                <MenuItem value="B">{t("units.B")}</MenuItem>
              </Select>
            </InputAdornment>
          }
        />
        <FormHelperText>{t("presets.min_file_size_hint")}</FormHelperText>
      </FormControl>
      <InputLabel>
        <Checkbox
          checked={createSubDir}
          onChange={(e) => setCreateSubDir(e.target.checked)}
        />{" "}
        {t("presets.create_sub_dir")}
      </InputLabel>
    </>
  );
};

export default PresetForm;
