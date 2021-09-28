import { Theme, makeStyles } from "@material-ui/core";
import CloseIcon from "@material-ui/icons/Close";
import CheckIcon from "@material-ui/icons/Check";
import clsx from "clsx";
import { FC } from "react";

type UseStyleProps = {
  color?: "success" | "error";
  height?: number;
};

const useStyle = makeStyles<Theme, UseStyleProps>((theme) => ({
  root: (props) => ({
    height: props.height || 40,
    width: "100%",
    backgroundColor: theme.palette[props.color || "primary"].light,
    flexDirection: "row",
    display: "flex",
    overflow: "hidden",
  }),
  step: (props) => ({
    position: "relative",
    overflow: "visible",
    height: "100%",
    flex: 1,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: theme.palette[props.color || "primary"].light,
    color: theme.palette[props.color || "primary"].contrastText,
    ...theme.typography.button,
    "& svg": {
      height: 16,
    },
  }),
  active: (props) => ({
    backgroundColor: theme.palette[props.color || "primary"].main,
    "&:before": {
      backgroundColor: theme.palette[props.color || "primary"].main,
    },
  }),
}));

type ProgressBarProps = {
  type?: "success" | "error" | "progress";
  progress?: number;
  step: number;
  stepCount: number;
};
const ProgressBar: FC<ProgressBarProps> = ({
  type = "progress",
  progress,
  step,
  stepCount,
}) => {
  const classes = useStyle({
    color:
      type === "success" ? "success" : type === "error" ? "error" : undefined,
    height: 16,
  });

  return (
    <div className={classes.root}>
      {Array(stepCount)
        .fill(0)
        .map((_, index) => (
          <div
            key={index}
            className={clsx(classes.step, step >= index + 1 && classes.active)}
          >
            {step === index + 1 &&
              (type === "success" ? (
                <CheckIcon />
              ) : type === "error" ? (
                <CloseIcon />
              ) : progress != null ? (
                <span>{progress}%</span>
              ) : (
                <ThreeDots />
              ))}
            {step > index + 1 && <CheckIcon />}
          </div>
        ))}
    </div>
  );
};

export default ProgressBar;

const useDotsStyle = makeStyles((theme) => ({
  "@keyframes pulse": {
    from: { opacity: 0.33 },
    to: { opacity: 1 },
  },
  dots: {
    display: "flex",
    alignItem: "center",
    justifyContent: "center",
    "& span": {
      backgroundColor: theme.palette.primary.contrastText,
      width: 6,
      height: 6,
      borderRadius: "50%",
      opacity: 0.67,
      animation: "$pulse 1s infinite alternate",
      animationDelay: ".5s",
    },
    "& span:not(:last-child)": {
      marginRight: 3,
    },
    "& span:last-child": {
      animationDelay: "1s",
    },
    "& span:first-child": {
      animationDelay: "0s",
    },
  },
}));

const ThreeDots = () => {
  const classes = useDotsStyle();
  return (
    <span className={classes.dots}>
      <span></span>
      <span></span>
      <span></span>
    </span>
  );
};
