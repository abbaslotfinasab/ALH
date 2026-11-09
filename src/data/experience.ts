export const professionalExperience = [
  {
    company: "SwanTech",
    roles: [
      {
        title: "Android Team Lead",
        summary:
          "هدایت فنی تیم اندروید و مشارکت در تصمیم‌های معماری و توسعه محصول.",
      },
      {
        title: "Technical Manager",
        summary:
          "گسترش مسئولیت‌ها از توسعه موبایل به هماهنگی فنی و تصمیم‌گیری‌های کلان‌تر محصول و تیم.",
      },
    ],
    focus: ["Android", "Team Leadership", "Technical Strategy"],
  },
  {
    company: "Utechia",
    roles: [
      {
        title: "Mobile Software Developer",
        summary:
          "توسعه اپلیکیشن‌های موبایل Android و iOS با Kotlin Multiplatform؛ مشارکت در ساخت یک اپلیکیشن سازمانی با قابلیت‌های خدمات کارکنان.",
      },
    ],
    focus: ["Kotlin Multiplatform", "Android", "iOS"],
  },
] as const;

export const selectedProjects = [
  {
    name: "Piston",
    category: "Mobile Product",
    summary:
      "توسعه اپلیکیشن اندروید با تمرکز بر Jetpack Compose و Clean Architecture.",
    technologies: ["Kotlin", "Jetpack Compose", "Clean Architecture"],
  },
  {
    name: "Vinsel ICDL",
    category: "Digital Product",
    summary:
      "یکی از پروژه‌های محصولی در مسیر توسعه نرم‌افزار و تجربه کاربری.",
    technologies: [],
  },
] as const;
