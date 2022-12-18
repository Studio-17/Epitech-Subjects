// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require('prism-react-renderer/themes/github');
const darkCodeTheme = require('prism-react-renderer/themes/dracula');

const organizationName= 'Studio-17';
const projectName = 'Epitech-Subjects';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Epitech Subjects',
  tagline: 'The best repo for Epitech subjects',
  url: 'https://studio-17.github.io/',
  baseUrl: '/Epitech-Subjects/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/studio17-logo-noel.ico',
  // GitHub Pages adds a trailing slash by default that I don't want
  trailingSlash: false,


  // GitHub pages deployment config.
  organizationName, // GitHub org/user name.
  projectName, // repo name.

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: 'Epitech Subjects',
        logo: {
          alt: 'Studio 17 Logo',
          src: 'img/studio17-logo-noel.png',
        },
        items: [
          {
            type: 'doc',
            docId: 'intro',
            position: 'left',
            label: 'Subjects',
          },
          {
            href: `https://github.com/${organizationName}/${projectName}`,
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        copyright: `Made by the ${organizationName}`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
    }),
};

module.exports = config;
