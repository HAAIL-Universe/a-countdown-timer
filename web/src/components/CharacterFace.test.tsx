import { render } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { CharacterFace } from "./CharacterFace";

describe("CharacterFace", () => {
  describe("renders happy expression for urgencyLevel 0", () => {
    it("displays gold face with happy eyes and smile", () => {
      render(<CharacterFace urgencyLevel={0} status="idle" />);

      const svg = document.querySelector("svg");
      expect(svg).toBeInTheDocument();

      const faceCircle = svg?.querySelector("circle[r='90']");
      expect(faceCircle).toHaveAttribute("fill", "#FFD700");

      const smilePath = svg?.querySelector('path[d*="M 60 120 Q 100 150 140 120"]');
      expect(smilePath).toBeInTheDocument();
    });

    it("renders happy eyes (black circles with white highlights)", () => {
      render(<CharacterFace urgencyLevel={0} status="idle" />);

      const svg = document.querySelector("svg");
      const circles = Array.from(svg?.querySelectorAll("circle") || []);
      const happyEyes = circles.filter(
        (c) =>
          c.getAttribute("fill") === "#000" &&
          c.getAttribute("r") === "12" &&
          (c.getAttribute("cx") === "70" || c.getAttribute("cx") === "130") &&
          c.getAttribute("cy") === "70"
      );
      expect(happyEyes.length).toBe(2);

      const highlights = circles.filter(
        (c) =>
          c.getAttribute("fill") === "#FFF" &&
          c.getAttribute("r") === "4" &&
          (c.getAttribute("cx") === "72" || c.getAttribute("cx") === "132") &&
          c.getAttribute("cy") === "68"
      );
      expect(highlights.length).toBe(2);
    });
  });

  describe("renders anxious expression for urgencyLevel 2", () => {
    it("displays orange face with crossed eyes and neutral mouth", () => {
      render(<CharacterFace urgencyLevel={2} status="running" />);

      const svg = document.querySelector("svg");
      expect(svg).toBeInTheDocument();

      const faceCircle = svg?.querySelector("circle[r='90']");
      expect(faceCircle).toHaveAttribute("fill", "#FFA500");

      const neutralMouth = svg?.querySelector('path[d*="M 60 130 Q 100 125 140 130"]');
      expect(neutralMouth).toBeInTheDocument();
    });

    it("renders anxious eyes (ellipses with crosshair lines)", () => {
      render(<CharacterFace urgencyLevel={2} status="running" />);

      const svg = document.querySelector("svg");
      const ellipses = Array.from(svg?.querySelectorAll("ellipse") || []);
      const anxiousEyes = ellipses.filter(
        (e) =>
          e.getAttribute("stroke") === "#000" &&
          e.getAttribute("rx") === "14" &&
          e.getAttribute("ry") === "18" &&
          (e.getAttribute("cx") === "70" || e.getAttribute("cx") === "130") &&
          e.getAttribute("cy") === "70"
      );
      expect(anxiousEyes.length).toBe(2);

      const crossLines = Array.from(svg?.querySelectorAll("line") || []).filter(
        (line) => line.getAttribute("stroke-width") === "2"
      );
      expect(crossLines.length).toBeGreaterThan(0);
    });
  });

  describe("renders upset expression for urgencyLevel 3", () => {
    it("displays red face with X eyes and sad mouth", () => {
      render(<CharacterFace urgencyLevel={3} status="paused" />);

      const svg = document.querySelector("svg");
      expect(svg).toBeInTheDocument();

      const faceCircle = svg?.querySelector("circle[r='90']");
      expect(faceCircle).toHaveAttribute("fill", "#FF6B6B");

      const sadMouth = svg?.querySelector('path[d*="M 60 140 Q 100 120 140 140"]');
      expect(sadMouth).toBeInTheDocument();
    });

    it("renders upset eyes (X marks with thick lines)", () => {
      render(<CharacterFace urgencyLevel={3} status="paused" />);

      const svg = document.querySelector("svg");
      const lines = Array.from(svg?.querySelectorAll('line[stroke="#000"][stroke-width="4"]') || []);
      expect(lines.length).toBeGreaterThan(0);

      const leftEyeX = lines.some(
        (line) =>
          (line.getAttribute("x1") === "55" && line.getAttribute("y1") === "55") ||
          (line.getAttribute("x1") === "85" && line.getAttribute("y1") === "55")
      );
      expect(leftEyeX).toBe(true);

      const rightEyeX = lines.some(
        (line) =>
          (line.getAttribute("x1") === "115" && line.getAttribute("y1") === "55") ||
          (line.getAttribute("x1") === "145" && line.getAttribute("y1") === "55")
      );
      expect(rightEyeX).toBe(true);
    });
  });

  describe("animation classes", () => {
    it("applies animate-pulse class when status is running", () => {
      render(<CharacterFace urgencyLevel={1} status="running" />);

      const container = document.querySelector(".animate-pulse");
      expect(container).toBeInTheDocument();
    });

    it("does not apply animate-pulse when status is idle", () => {
      const { container } = render(<CharacterFace urgencyLevel={0} status="idle" />);

      expect(container.querySelector(".animate-pulse")).not.toBeInTheDocument();
    });

    it("applies animate-bounce to SVG when upset (urgencyLevel 3)", () => {
      render(<CharacterFace urgencyLevel={3} status="running" />);

      const svg = document.querySelector(".animate-bounce");
      expect(svg).toBeInTheDocument();
    });

    it("does not apply animate-bounce when happy (urgencyLevel 0)", () => {
      render(<CharacterFace urgencyLevel={0} status="running" />);

      const svg = document.querySelector("svg");
      expect(svg).not.toHaveClass("animate-bounce");
    });
  });

  describe("fallback behavior", () => {
    it("renders happy face for urgencyLevel 1 (unmapped level)", () => {
      render(<CharacterFace urgencyLevel={1} status="idle" />);

      const faceCircle = document.querySelector("circle[r='90']");
      expect(faceCircle).toHaveAttribute("fill", "#FFD700");

      const smilePath = document.querySelector('path[d*="M 60 120 Q 100 150 140 120"]');
      expect(smilePath).toBeInTheDocument();
    });

    it("renders happy face for urgencyLevel > 3 (unmapped level)", () => {
      render(<CharacterFace urgencyLevel={5} status="idle" />);

      const faceCircle = document.querySelector("circle[r='90']");
      expect(faceCircle).toHaveAttribute("fill", "#FFD700");
    });
  });

  describe("SVG structure", () => {
    it("always renders an SVG element", () => {
      render(<CharacterFace urgencyLevel={0} status="idle" />);

      const svg = document.querySelector("svg");
      expect(svg).toBeInTheDocument();
      expect(svg).toHaveAttribute("width", "200");
      expect(svg).toHaveAttribute("height", "200");
    });

    it("renders face circle with black stroke", () => {
      render(<CharacterFace urgencyLevel={2} status="running" />);

      const faceCircle = document.querySelector("circle[r='90']");
      expect(faceCircle).toHaveAttribute("stroke", "#000");
      expect(faceCircle).toHaveAttribute("stroke-width", "3");
    });
  });
});
