import { ChangeEvent, useEffect, useRef, useState } from "react";
import { Checkbox, Chip, FormControl, FormHelperText, Input, InputAdornment, InputLabel, MenuItem, Select, TextField } from "@material-ui/core";
import { useTranslation } from "react-i18next";
import { Preset } from "../../models/presets.type";
import { Autocomplete } from "@material-ui/lab";

type PresetProps = {
    preset: Preset,
    onUpdate: (p:Preset) => void
};

const ALL_EXTENSIONS = "___all___";

const PresetForm:React.FC<PresetProps>= ({preset, onUpdate}) => {
    const {t} = useTranslation();
    const didMount = useRef(false);
    const [name, setName] = useState(preset.name || "");
    const [watchDir, setWatchDir] = useState(preset.watch_dir || "");
    const [outputDir, setOutputDir] = useState(preset.output_dir || "");
    const [minFileSizeStr, setMinFileSizeStr] = useState(""+(preset.min_file_size || 0));
    const [minFileSizeUnit, setMinFileSizeUnit] = useState(1);
    const [minFileSize, setMinFileSize] = useState(preset.min_file_size || 0);
    const [createSubDir, setCreateSubDir] = useState(preset.create_sub_dir || false);
    const [extensions, setExtensions] = useState(preset.file_extensions ? [...preset.file_extensions] : [ALL_EXTENSIONS]);

    const cleanMinFileSize = () => {
        const minFileSize = minFileSizeStr.length > 0 ? parseInt(minFileSizeStr, 10) :  0;
        if (minFileSize > 0) {
            let tmpFileSize = minFileSize * minFileSizeUnit;
            let curUnit = 1e12;
            while(!Number.isInteger(tmpFileSize/curUnit)) {
                curUnit /= 1e3;
            }
            setMinFileSizeStr(""+(tmpFileSize/curUnit));
            setMinFileSizeUnit(curUnit);
        } else {
            setMinFileSizeUnit(1);
        }

        if( minFileSizeStr.length === 0) {
            setMinFileSizeStr("0");
        }
    };

    useEffect(cleanMinFileSize, [preset.min_file_size]);

    useEffect(() => {
        const newMinFileSize = (minFileSizeStr.length > 0 ? parseInt(minFileSizeStr, 10) :  0)*minFileSizeUnit;
        setMinFileSize(newMinFileSize);
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
                file_extensions: exts.length ? exts : null
            };
            cleanMinFileSize();
            onUpdate(newPreset);
        } else {
            didMount.current = true;
        }
    }, [name, watchDir, outputDir, minFileSize, createSubDir, extensions]);


    const handleChangeMinFileSizeUnit = (e:ChangeEvent<{ value: unknown }>) => {
        setMinFileSizeUnit(parseInt(e.target.value as string, 10));
    }

    const handleUpdateExtensions = (e:ChangeEvent<{ }>, value: string[]) => {
        if(value.indexOf(ALL_EXTENSIONS) >= 0) {
            value.splice(value.indexOf(ALL_EXTENSIONS), 1);
        }
        setExtensions(value.length === 0 ? [ALL_EXTENSIONS] : value);
    };

    return <>
        <TextField
            label={t("presets.name")}
            defaultValue={name}
            onChange={(e) => setName(e.target.value)}
            fullWidth={true} />
        <TextField
            label={t("presets.watch_dir")}
            defaultValue={watchDir}
            onChange={(e) => setWatchDir(e.target.value)}
            fullWidth={true} />
        <TextField
            label={t("presets.output_dir")}
            defaultValue={outputDir}
            onChange={(e) => setOutputDir(e.target.value)}
            fullWidth={true} />
        <Autocomplete multiple
            options={[] as string[]} freeSolo
            value={extensions}
            onChange={handleUpdateExtensions}
            renderTags={(value: string[], getTagProps) =>
                value.map((option: string, index: number) => option === ALL_EXTENSIONS ? <Chip variant="outlined" label={t("presets.all")} key={index} /> : <Chip variant="outlined" label={option} {...getTagProps({ index })} />)
            }
            renderInput={(params) => (
                <TextField {...params} label={t("presets.file_extensions")} fullWidth />
            )}
        />
        <FormControl fullWidth={true} >
          <InputLabel htmlFor={`preset-min-file-size-${preset.name}`}>{t("presets.min_file_size")}</InputLabel>
          <Input
            id={`preset-min-file-size-${preset.name}`}
            value={minFileSizeStr}
            onChange={(e) => setMinFileSizeStr(e.target.value)}
            endAdornment={<InputAdornment position="end">
                <Select onChange={handleChangeMinFileSizeUnit} value={minFileSizeUnit}>
                  <MenuItem value={1e12}>{t("units.TB")}</MenuItem>
                  <MenuItem value={1e9}>{t("units.GB")}</MenuItem>
                  <MenuItem value={1e6}>{t("units.MB")}</MenuItem>
                  <MenuItem value={1e3}>{t("units.KB")}</MenuItem>
                  <MenuItem value={1}>{t("units.B")}</MenuItem>
                </Select>
              </InputAdornment>
            }
          />
          <FormHelperText>{t("presets.min_file_size_hint")}</FormHelperText>
        </FormControl>
        <InputLabel>
            <Checkbox checked={createSubDir} onChange={(e) => setCreateSubDir(e.target.checked)} /> {t("presets.create_sub_dir")}
        </InputLabel>
    </>;
}

export default PresetForm;