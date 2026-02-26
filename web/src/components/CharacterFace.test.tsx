import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { CharacterFace } from "./CharacterFace";
import { TimerStatus } from "../types/timer";

describe("CharacterFace", () => {
  const getEllipsesInSvg = () => {
    const svg = screen.getByRole("img", { hidden: true });
    return svg.querySelectorAll("ellipse");
  };

  const getPathsInSvg = () => {
    const svg = screen.getByRole("img", { hidden: true });
    return svg.querySelectorAll("path");
  };

  const getCirclesInSvg = () => {
    const svg = screen.getByRole("img", { hidden: true });
    return svg.querySelectorAll("circle");
  };

  describe("renders happy expression", () => {
    it("renders happy face for urgencyLevel 0", () => {
      render(<CharacterFace urgencyLevel={0} status="idle" />);

      const circles = getCirclesInSvg();
      expect(circles.length).toBeGreaterThanOrEqual(6);

      const paths = getPathsInSvg();
      const mouthPath = paths[0];
      expect(mouthPath).toBeDefined();
      expect(mouthPath.getAttribute("d")).toMatch(/M 45 75 Q 60 85 75 75/);
    });

    it("renders happy face when status is idle regardless of urgencyLevel", () => {
      render(<CharacterFace urgencyLevel={2} status="idle" />);

      const paths = getPathsInSvg();
      const mouthPath = paths[0];
      expect(mouthPath.getAttribute("d")).toMatch(/M 45 75 Q 60 85 75 75/);
    });

    it("renders happy eyes (circles) for urgencyLevel 0", () => {
      render(<CharacterFace urgencyLevel={0} status="running" />);

      const circles = getCirclesInSvg();
      expect(circles.length).toBeGreaterThanOrEqual(6);

      const eyeCircles = Array.from(circles).filter(
        (c) =>
          c.getAttribute("cx") === "40" || c.getAttribute("cx") === "80"
      );
      expect(eyeCircles.length).toBeGreaterThanOrEqual(4);

      const leftEyeOuter = eyeCircles.find(
        (c) => c.getAttribute("cx") === "40" && c.getAttribute("r") === "8"
      );
      expect(leftEyeOuter).toBeDefined();
    });
  });

  describe("renders anxious expression", () => {
    it("renders anxious face for urgencyLevel 2", () => {
      render(<CharacterFace urgencyLevel={2} status="running" />);

      const paths = getPathsInSvg();
      const mouthPath = paths[0];
      expect(mouthPath).toBeDefined();
      expect(mouthPath.getAttribute("d")).toMatch(/M 45 80 L 60 70 L 75 80/);
    });

    it("renders anxious eyes (ellipses) for urgencyLevel 2", () => {
      render(<CharacterFace urgencyLevel={2} status="running" />);

      const ellipses = getEllipsesInSvg();
      expect(ellipses.length).toBeGreaterThanOrEqual(4);

      const leftEyeEllipse = Array.from(ellipses).find(
        (e) => e.getAttribute("cx") === "40" && e.getAttribute("ry") === "10"
      );
      expect(leftEyeEllipse).toBeDefined();
      expect(leftEyeEllipse?.getAttribute("rx")).toBe("7");

      const rightEyeEllipse = Array.from(ellipses).find(
        (e) => e.getAttribute("cx") === "80" && e.getAttribute("ry") === "10"
      );
      expect(rightEyeEllipse).toBeDefined();
      expect(rightEyeEllipse?.getAttribute("rx")).toBe("7");
    });

    it("renders anxious face for urgencyLevel 2.5", () => {
      render(<CharacterFace urgencyLevel={2.5} status="paused" />);

      const paths = getPathsInSvg();
      const mouthPath = paths[0];
      expect(mouthPath.getAttribute("d")).toMatch(/M 45 80 L 60 70 L 75 80/);
    });
  });

  describe("renders upset expression", () => {
    it("renders upset face for urgencyLevel 3", () => {
      render(<CharacterFace urgencyLevel={3} status="running" />);

      const paths = getPathsInSvg();
      const mouthPath = paths[0];
      expect(mouthPath).toBeDefined();
      expect(mouthPath.getAttribute("d")).toMatch(/M 45 70 Q 60 60 75 70/);
    });

    it("renders upset eyes (rotated ellipses) for urgencyLevel 3", () => {
      render(<CharacterFace urgencyLevel={3} status="running" />);

      const ellipses = getEllipsesInSvg();
      expect(ellipses.length).toBeGreaterThanOrEqual(4);

      const leftEyeEllipse = Array.from(ellipses).find(
        (e) => e.getAttribute("cx") === "40" && e.getAttribute("ry") === "4"
      );
      expect(leftEyeEllipse).toBeDefined();
      expect(leftEyeEllipse?.getAttribute("transform")).toMatch(/-15/);

      const rightEyeEllipse = Array.from(ellipses).find(
        (e) => e.getAttribute("cx") === "80" && e.getAttribute("ry") === "4"
      );
      expect(rightEyeEllipse).toBeDefined();
      expect(rightEyeEllipse?.getAttribute("transform")).toMatch(/15/);
    });

    it("renders upset face for urgencyLevel 5", () => {
      render(<CharacterFace urgencyLevel={5} status="complete" />);

      const paths = getPathsInSvg();
      const mouthPath = paths[0];
      expect(mouthPath.getAttribute("d")).toMatch(/M 45 70 Q 60 60 75 70/);
    });
  });

  describe("urgencyLevel edge cases", () => {
    it("renders happy for urgencyLevel 1 (less than 2)", () => {
      render(<CharacterFace urgencyLevel={1} status="running" />);

      const circles = getCirclesInSvg();
      const eyeCircles = Array.from(circles).filter(
        (c) =>
          c.getAttribute("cx") === "40" || c.getAttribute("cx") === "80"
      );
      expect(eyeCircles.length).toBeGreaterThanOrEqual(4);
    });

    it("renders anxious for urgencyLevel exactly 2", () => {
      render(<CharacterFace urgencyLevel={2} status="running" />);

      const ellipses = getEllipsesInSvg();
      const anxiousEye = Array.from(ellipses).find(
        (e) => e.getAttribute("ry") === "10"
      );
      expect(anxiousEye).toBeDefined();
    });

    it("renders upset for urgencyLevel 3 (not anxious)", () => {
      render(<CharacterFace urgencyLevel={3} status="running" />);

      const ellipses = getEllipsesInSvg();
      const upsetEye = Array.from(ellipses).find(
        (e) => e.getAttribute("ry") === "4"
      );
      expect(upsetEye).toBeDefined();

      const anxiousEye = Array.from(ellipses).find(
        (e) => e.getAttribute("ry") === "10"
      );
      expect(anxiousEye).toBeUndefined();
    });
  });

  describe("renders SVG structure", () => {
    it("renders SVG with correct dimensions", () => {
      render(<CharacterFace urgencyLevel={0} status="idle" />);

      const svg = screen.getByRole("img", { hidden: true });
      expect(svg).toHaveAttribute("width", "120");
      expect(svg).toHaveAttribute("height", "120");
      expect(svg).toHaveAttribute("viewBox", "0 0 120 120");
    });

    it("renders face circle with yellow fill", () => {
      render(<CharacterFace urgencyLevel={0} status="idle" />);

      const circles = getCirclesInSvg();
      const faceCircle = Array.from(circles).find(
        (c) => c.getAttribute("cx") === "60" && c.getAttribute("cy") === "60"
      );
      expect(faceCircle).toBeDefined();
      expect(faceCircle?.getAttribute("fill")).toBe("#FFD700");
    });

    it("renders container with correct classes", () => {
      render(<CharacterFace urgencyLevel={0} status="idle" />);

      const container = screen.getByRole("img", { hidden: true }).parentElement;
      expect(container).toHaveClass("flex");
      expect(container).toHaveClass("justify-center");
      expect(container).toHaveClass("items-center");
      expect(container).toHaveClass("py-6");
    });

    it("renders SVG with drop-shadow class", () => {
      render(<CharacterFace urgencyLevel={0} status="idle" />);

      const svg = screen.getByRole("img", { hidden: true });
      expect(svg).toHaveClass("drop-shadow-lg");
    });
  });

  describe("status prop edge cases", () => {
    it("renders happy face when status is running and urgencyLevel is 0", () => {
      render(<CharacterFace urgencyLevel={0} status="running" />);

      const circles = getCirclesInSvg();
      const eyeCircles = Array.from(circles).filter(
        (c) =>
          c.getAttribute("cx") === "40" || c.getAttribute("cx") === "80"
      );
      expect(eyeCircles.length).toBeGreaterThanOrEqual(4);
    });

    it("renders anxious face when status is paused and urgencyLevel is 2", () => {
      render(<CharacterFace urgencyLevel={2} status="paused" />);

      const ellipses = getEllipsesInSvg();
      const anxiousEye = Array.from(ellipses).find(
        (e) => e.getAttribute("ry") === "10"
      );
      expect(anxiousEye).toBeDefined();
    });

    it("respects status idle override for happy expression", () => {
      render(<CharacterFace urgencyLevel={3} status="idle" />);

      const paths = getPathsInSvg();
      const mouthPath = paths[0];
      expect(mouthPath.getAttribute("d")).toMatch(/M 45 75 Q 60 85 75 75/);
    });
  });
});
